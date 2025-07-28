"""EPUB Chinese vocabulary analysis functionality."""

import re
import logging
import json
import hashlib
import os
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Set, NamedTuple, Optional, Tuple
import math

try:
    import ebooklib
    from ebooklib import epub

    EBOOKLIB_AVAILABLE = True
except ImportError:
    EBOOKLIB_AVAILABLE = False

try:
    from azure.ai.textanalytics import TextAnalyticsClient
    from azure.core.credentials import AzureKeyCredential

    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

try:
    from pypinyin import lazy_pinyin, Style

    PYPINYIN_AVAILABLE = True
except ImportError:
    PYPINYIN_AVAILABLE = False

from .hsk import HSKWordLists

logger = logging.getLogger(__name__)


class VocabularyStats(NamedTuple):
    """Statistics for vocabulary analysis."""

    total_words: int
    unique_words: int
    chinese_words: int
    unique_chinese_words: int


class HSKDistribution(NamedTuple):
    """HSK level distribution statistics."""

    level: int
    word_count: int
    unique_count: int
    percentage: float
    coverage_percentage: float


class CoverageTarget(NamedTuple):
    """Coverage target calculation results."""

    target_percentage: float
    words_needed: int
    current_coverage: float
    priority_words: List[Tuple[str, int, str, Optional[int]]]  # (word, frequency, pinyin, hsk_level)


class HSKLearningTarget(NamedTuple):
    """HSK level learning recommendations."""

    level: int
    unknown_words: List[Tuple[str, int, str]]  # (word, frequency, pinyin) ordered by frequency
    potential_coverage_gain: float  # percentage coverage gained if all words learned
    total_word_count: int  # total occurrences of these words in text


class BookAnalysis(NamedTuple):
    """Complete book analysis results."""

    title: str
    stats: VocabularyStats
    word_frequencies: Dict[str, int]
    hsk_distribution: List[HSKDistribution]
    known_words: Set[str]
    unknown_words: Dict[str, int]  # word -> frequency
    high_frequency_unknown: List[Tuple[str, int, str, Optional[int]]]  # (word, frequency, pinyin, hsk_level)
    coverage_targets: Dict[int, CoverageTarget]  # target_percentage -> results
    non_hsk_words: Dict[str, int]  # words not in any HSK level -> frequency
    hsk_learning_targets: List[HSKLearningTarget]  # HSK-based learning suggestions


class ChineseEPUBAnalyzer:
    """Analyzer for Chinese vocabulary in EPUB files."""

    def __init__(
        self,
        hsk_word_lists: Optional[HSKWordLists] = None,
        cache_dir: Optional[Path] = None,
    ):
        """
        Initialize the EPUB analyzer.

        Args:
            hsk_word_lists: HSK word lists for level analysis
            cache_dir: Optional directory for caching Azure API results
        """
        if not EBOOKLIB_AVAILABLE:
            raise ImportError("ebooklib is required for EPUB analysis. " "Install it with: pip install ebooklib")

        if not AZURE_AVAILABLE:
            raise ImportError(
                "Azure Text Analytics is required for key phrase extraction. "
                "Install with: pip install azure-ai-textanalytics==5.3.0"
            )

        self.hsk_word_lists = hsk_word_lists or HSKWordLists()
        self.chinese_pattern = re.compile(r"[\u4e00-\u9fff]+")

        # Set up Azure credentials
        try:
            self.endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
            self.key = os.environ["AZURE_LANGUAGE_KEY"]
        except KeyError:
            raise ValueError("Please set the AZURE_LANGUAGE_ENDPOINT and " "AZURE_LANGUAGE_KEY environment variables.")

        # Initialize Azure Text Analytics client
        self.text_analytics_client = TextAnalyticsClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

        # Set up cache directory
        default_cache = Path.home() / ".anki_pleco_importer" / "azure_cache"
        self.cache_dir = cache_dir or default_cache
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Using Azure API cache directory: {self.cache_dir}")

    def extract_text_from_epub(self, epub_path: Path) -> Tuple[str, str]:
        """
        Extract text content from EPUB file.

        Args:
            epub_path: Path to the EPUB file

        Returns:
            Tuple of (title, full_text)
        """
        try:
            book = epub.read_epub(str(epub_path))

            # Get book title
            title = book.get_metadata("DC", "title")[0][0] if book.get_metadata("DC", "title") else "Unknown"

            # Extract text from all HTML documents
            full_text = []

            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    content = item.get_content().decode("utf-8", errors="ignore")

                    # Remove HTML tags and extract plain text
                    text = self._clean_html(content)
                    if text.strip():
                        full_text.append(text)

            combined_text = "\n".join(full_text)
            logger.info(f"Extracted {len(combined_text)} characters from '{title}'")

            return title, combined_text

        except Exception as e:
            logger.error(f"Failed to extract text from EPUB: {e}")
            raise

    def _clean_html(self, html_content: str) -> str:
        """
        Clean HTML content and extract plain text.

        Args:
            html_content: Raw HTML content

        Returns:
            Clean plain text
        """
        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", html_content)

        # Remove common HTML entities
        text = text.replace("&nbsp;", " ")
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&amp;", "&")
        text = text.replace("&quot;", '"')
        text = text.replace("&#39;", "'")

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _get_cache_key(self, text: str) -> str:
        """Generate a cache key for the given text."""
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def _load_from_cache(self, cache_key: str) -> Optional[List[str]]:
        """Load key phrases from cache if available."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logger.debug(f"📁 Loaded from cache: {cache_file.name}")
                    phrases = data.get("key_phrases", [])
                    return phrases if isinstance(phrases, list) else []
            except Exception as e:
                logger.warning(f"Failed to load cache file {cache_file}: {e}")
        return None

    def _smart_chunk_text(self, text: str, max_chunk_size: int) -> List[str]:
        """
        Split text into chunks respecting paragraph and sentence boundaries.

        Args:
            text: Input text to chunk
            max_chunk_size: Maximum size for each chunk

        Returns:
            List of text chunks with natural boundaries preserved
        """
        if len(text) <= max_chunk_size:
            return [text]

        chunks = []
        current_chunk = ""

        # Split by paragraphs first (double newlines, or common Chinese punctuation)
        paragraphs = re.split(r"\n\s*\n|。\s*\n|！\s*\n|？\s*\n", text)

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # If paragraph is small enough, add to current chunk
            if len(current_chunk) + len(paragraph) + 1 <= max_chunk_size:
                if current_chunk:
                    current_chunk += "\n" + paragraph
                else:
                    current_chunk = paragraph
            else:
                # Current chunk is ready, start new one
                if current_chunk:
                    chunks.append(current_chunk)

                # If paragraph itself is too large, split by sentences
                if len(paragraph) > max_chunk_size:
                    sentence_chunks = self._split_by_sentences(paragraph, max_chunk_size)
                    chunks.extend(sentence_chunks[:-1])  # Add all but last
                    current_chunk = sentence_chunks[-1] if sentence_chunks else ""
                else:
                    current_chunk = paragraph

        # Add final chunk
        if current_chunk:
            chunks.append(current_chunk)

        # Log chunk sizes for debugging
        chunk_sizes = [len(chunk) for chunk in chunks]
        logger.debug(f"Created {len(chunks)} chunks with sizes: {chunk_sizes}")

        return chunks

    def _split_by_sentences(self, text: str, max_chunk_size: int) -> List[str]:
        """
        Split text by sentence boundaries when paragraph is too large.

        Args:
            text: Input text to split
            max_chunk_size: Maximum size for each chunk

        Returns:
            List of sentence-based chunks
        """
        # Chinese sentence endings
        sentences = re.split(r"([。！？；])", text)

        chunks = []
        current_chunk = ""

        # Rejoin sentences with their punctuation
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i]
            if i + 1 < len(sentences):
                sentence += sentences[i + 1]  # Add punctuation

            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)

                # If single sentence is still too long, force split
                if len(sentence) > max_chunk_size:
                    # Split at max_chunk_size but try to find a comma or space near the boundary
                    while sentence:
                        if len(sentence) <= max_chunk_size:
                            current_chunk = sentence
                            break

                        # Look for a good break point near max_chunk_size
                        break_point = max_chunk_size
                        for punct in ["，", "、", " ", "的", "了", "在"]:
                            punct_pos = sentence.rfind(punct, max_chunk_size - 200, max_chunk_size)
                            if punct_pos > max_chunk_size - 500:  # Within reasonable range
                                break_point = punct_pos + len(punct)
                                break

                        chunks.append(sentence[:break_point])
                        sentence = sentence[break_point:].strip()

                    current_chunk = sentence
                else:
                    current_chunk = sentence

        # Add final chunk
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _save_to_cache(self, cache_key: str, key_phrases: List[str]) -> None:
        """Save key phrases to cache."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            data = {"key_phrases": key_phrases, "timestamp": time.time()}
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                logger.info(f"💾 Saved key phrases to cache: {cache_file}")
        except Exception as e:
            logger.warning(f"Failed to save cache file {cache_file}: {e}")

    def extract_key_phrases_from_text(self, text: str, min_length: int = 1, chunk_size: int = 5000) -> List[str]:
        """
        Extract key phrases from Chinese text using Azure Text Analytics.

        Args:
            text: Input Chinese text
            min_length: Minimum phrase length to include
            chunk_size: Maximum size of text chunks to send to Azure API

        Returns:
            List of extracted Chinese key phrases
        """
        # Extract Chinese characters only
        chinese_text = "".join(self.chinese_pattern.findall(text))

        if not chinese_text:
            return []

        # Check cache first
        cache_key = self._get_cache_key(chinese_text)
        cached_phrases = self._load_from_cache(cache_key)
        if cached_phrases is not None:
            logger.info("💾 Using cached key phrases (no API call needed)")
            return [phrase for phrase in cached_phrases if len(phrase) >= min_length]

        # Split text into chunks if too large, respecting text boundaries
        all_key_phrases = []
        text_chunks = self._smart_chunk_text(chinese_text, chunk_size)

        logger.info(f"Processing {len(text_chunks)} text chunks for extraction")

        for i, chunk in enumerate(text_chunks):
            if not chunk.strip():
                continue

            logger.info(f"🌐 Making Azure API call for chunk {i+1}/{len(text_chunks)} " f"(size: {len(chunk)} chars)")
            try:
                documents = [{"id": str(i), "language": "zh-hans", "text": chunk}]
                response = self.text_analytics_client.extract_key_phrases(documents=documents)
                logger.info(f"✅ Azure API call completed for chunk {i+1}")

                for doc in response:
                    if not doc.is_error:
                        for phrase in doc.key_phrases:
                            # Filter Chinese chars only and minimum length
                            if self.chinese_pattern.match(phrase) and len(phrase) >= min_length:
                                all_key_phrases.append(phrase)
                    else:
                        logger.error(f"Error processing text chunk {i}: " f"{doc.error.message}")

            except Exception as e:
                logger.error(f"❌ Azure API error for chunk {i+1}: {e}")
                continue

        # Remove duplicates while preserving order
        unique_phrases = list(dict.fromkeys(all_key_phrases))

        # Save to cache
        self._save_to_cache(cache_key, unique_phrases)

        logger.info(
            f"✨ Extracted {len(unique_phrases)} unique key phrases from text "
            f"({len(text_chunks)} Azure API calls made)"
        )
        return unique_phrases

    def count_phrase_frequencies_in_text(self, key_phrases: List[str], full_text: str) -> Dict[str, int]:
        """
        Count how many times each key phrase appears in the full text.
        Filters to only include 2-4 character words appearing 3+ times.

        Args:
            key_phrases: List of key phrases identified by Azure
            full_text: Original text from the EPUB

        Returns:
            Dictionary mapping filtered phrases to their frequencies in the text
        """
        phrase_frequencies = {}

        # Extract only Chinese characters from the full text for matching
        chinese_text = "".join(self.chinese_pattern.findall(full_text))

        for phrase in key_phrases:
            if not phrase:
                continue

            # Count occurrences of this phrase in the text
            # Use case-sensitive search since Chinese characters are case-sensitive
            count = chinese_text.count(phrase)

            # Filter: only keep 2-4 character words with frequency >= 3
            if count >= 3 and 2 <= len(phrase) <= 4:
                phrase_frequencies[phrase] = count

        logger.info(
            f"Found frequencies for {len(phrase_frequencies)} filtered key phrases (2-4 chars, 3+ occurrences) in text"
        )

        # Log some examples for debugging
        if phrase_frequencies:
            # Sort by length first (longest first), then by frequency (descending)
            sorted_phrases = sorted(phrase_frequencies.items(), key=lambda x: (-len(x[0]), -x[1]))
            top_phrases = sorted_phrases[:10]
            logger.debug(f"Sample phrases by length: {top_phrases}")

        return phrase_frequencies

    def get_word_pinyin(self, word: str) -> str:
        """
        Get pinyin for a Chinese word.

        Args:
            word: Chinese word to get pinyin for

        Returns:
            Pinyin string with tone marks
        """
        if not PYPINYIN_AVAILABLE:
            return ""

        try:
            # Use pypinyin to get pinyin with tone marks
            pinyin_list = lazy_pinyin(word, style=Style.TONE)
            return "".join(pinyin_list)
        except Exception:
            return ""

    def get_word_hsk_level(self, word: str) -> Optional[int]:
        """
        Get the HSK level of a Chinese word.

        Args:
            word: Chinese word to look up

        Returns:
            HSK level (1-7) if found, None if not in HSK lists
        """
        for level in self.hsk_word_lists.get_available_levels():
            hsk_words = self.hsk_word_lists.get_words_for_level(level)
            if word in hsk_words:
                return level
        return None

    def analyze_vocabulary_frequency(self, words: List[str]) -> Dict[str, int]:
        """
        Analyze word frequency in the text.

        Args:
            words: List of words to analyze

        Returns:
            Dictionary mapping words to their frequencies
        """
        return dict(Counter(words))

    def calculate_hsk_distribution(self, word_frequencies: Dict[str, int]) -> List[HSKDistribution]:
        """
        Calculate distribution of words across HSK levels.

        Args:
            word_frequencies: Word frequency dictionary

        Returns:
            List of HSK distribution statistics
        """
        total_words = sum(word_frequencies.values())
        total_unique = len(word_frequencies)

        distributions = []

        for level in self.hsk_word_lists.get_available_levels():
            hsk_words = self.hsk_word_lists.get_words_for_level(level)

            # Count words and frequency at this level
            level_word_count = 0
            level_unique_count = 0

            for word, freq in word_frequencies.items():
                if word in hsk_words:
                    level_word_count += freq
                    level_unique_count += 1

            # Calculate percentages
            percentage = (level_word_count / total_words * 100) if total_words > 0 else 0
            coverage_percentage = (level_unique_count / total_unique * 100) if total_unique > 0 else 0

            distributions.append(
                HSKDistribution(
                    level=level,
                    word_count=level_word_count,
                    unique_count=level_unique_count,
                    percentage=percentage,
                    coverage_percentage=coverage_percentage,
                )
            )

        return distributions

    def compare_with_anki_collection(
        self, word_frequencies: Dict[str, int], anki_words: Set[str]
    ) -> Tuple[Set[str], Dict[str, int]]:
        """
        Compare book vocabulary with Anki collection.

        Args:
            word_frequencies: Word frequency dictionary from book
            anki_words: Set of words in Anki collection

        Returns:
            Tuple of (known_words, unknown_words_with_frequency)
        """
        known_words = set()
        unknown_words = {}

        for word, freq in word_frequencies.items():
            if word in anki_words:
                known_words.add(word)
            else:
                unknown_words[word] = freq

        return known_words, unknown_words

    def calculate_coverage_targets(
        self,
        word_frequencies: Dict[str, int],
        known_words: Set[str],
        targets: List[int] = [80, 90, 95, 98],
    ) -> Dict[int, CoverageTarget]:
        """
        Calculate words needed to achieve target coverage percentages.

        Args:
            word_frequencies: Word frequency dictionary
            known_words: Set of words already known
            targets: List of target coverage percentages

        Returns:
            Dictionary mapping target percentages to coverage target results
        """
        # Sort unknown words by frequency (descending)
        unknown_words = {word: freq for word, freq in word_frequencies.items() if word not in known_words}
        sorted_unknown = sorted(unknown_words.items(), key=lambda x: x[1], reverse=True)

        total_words = sum(word_frequencies.values())
        known_word_count = sum(freq for word, freq in word_frequencies.items() if word in known_words)
        current_coverage = (known_word_count / total_words * 100) if total_words > 0 else 0

        results = {}

        for target in targets:
            target_word_count = math.ceil(total_words * target / 100)

            # Find priority words to reach target
            priority_words = []
            cumulative_freq = known_word_count

            for word, freq in sorted_unknown:
                if cumulative_freq >= target_word_count:
                    break
                pinyin = self.get_word_pinyin(word)
                hsk_level = self.get_word_hsk_level(word)
                priority_words.append((word, freq, pinyin, hsk_level))
                cumulative_freq += freq

            # Sort priority words by length first (longest first), then by frequency
            priority_words.sort(key=lambda x: (-len(x[0]), -x[1]))

            results[target] = CoverageTarget(
                target_percentage=target,
                words_needed=len(priority_words),
                current_coverage=current_coverage,
                priority_words=priority_words,
            )

        return results

    def get_high_frequency_unknown_words(
        self, unknown_words: Dict[str, int], count: int = 50
    ) -> List[Tuple[str, int, str, Optional[int]]]:
        """
        Get the most frequent unknown words, sorted by length then frequency.

        Args:
            unknown_words: Dictionary of unknown words with frequencies
            count: Number of words to return

        Returns:
            List of (word, frequency, pinyin, hsk_level) tuples sorted by length then frequency
        """
        # Sort by length first (longest first), then by frequency (descending)
        sorted_words = sorted(unknown_words.items(), key=lambda x: (-len(x[0]), -x[1]))[:count]
        return [
            (
                word,
                freq,
                self.get_word_pinyin(word),
                self.get_word_hsk_level(word),
            )
            for word, freq in sorted_words
        ]

    def identify_non_hsk_words(self, word_frequencies: Dict[str, int]) -> Dict[str, int]:
        """
        Identify words that are not in any HSK level.

        Args:
            word_frequencies: Word frequency dictionary

        Returns:
            Dictionary of non-HSK words with their frequencies
        """
        # Get all HSK words from all levels
        all_hsk_words = set()
        for level in self.hsk_word_lists.get_available_levels():
            all_hsk_words.update(self.hsk_word_lists.get_words_for_level(level))

        # Find words not in any HSK level
        non_hsk_words = {}
        for word, freq in word_frequencies.items():
            if word not in all_hsk_words:
                non_hsk_words[word] = freq

        return non_hsk_words

    def calculate_hsk_learning_targets(
        self, word_frequencies: Dict[str, int], known_words: Set[str]
    ) -> List[HSKLearningTarget]:
        """
        Calculate HSK-based learning recommendations.

        Args:
            word_frequencies: Word frequency dictionary from book
            known_words: Set of words already known

        Returns:
            List of HSK learning targets with unknown words and coverage gains
        """
        total_words = sum(word_frequencies.values())
        learning_targets = []

        for level in self.hsk_word_lists.get_available_levels():
            hsk_words = self.hsk_word_lists.get_words_for_level(level)

            # Find unknown words at this HSK level, ordered by frequency
            unknown_at_level = []
            total_word_count = 0

            for word, freq in word_frequencies.items():
                if word in hsk_words and word not in known_words:
                    pinyin = self.get_word_pinyin(word)
                    unknown_at_level.append((word, freq, pinyin))
                    total_word_count += freq

            # Sort by length first (longest first), then by frequency (descending)
            unknown_at_level.sort(key=lambda x: (-len(x[0]), -x[1]))

            # Calculate potential coverage gain
            potential_coverage_gain = (total_word_count / total_words * 100) if total_words > 0 else 0

            if unknown_at_level:  # Only include levels with unknown words
                learning_targets.append(
                    HSKLearningTarget(
                        level=level,
                        unknown_words=unknown_at_level,
                        potential_coverage_gain=potential_coverage_gain,
                        total_word_count=total_word_count,
                    )
                )

        return learning_targets

    def analyze_epub(
        self,
        epub_path: Path,
        anki_words: Set[str],
        min_frequency: int = 1,
        target_coverages: List[int] = [80, 90, 95, 98],
        top_unknown_count: int = 50,
    ) -> BookAnalysis:
        """
        Perform comprehensive analysis of an EPUB file.

        Args:
            epub_path: Path to the EPUB file
            anki_words: Set of words in user's Anki collection
            min_frequency: Minimum frequency threshold for analysis
            target_coverages: List of target coverage percentages
            top_unknown_count: Number of top unknown words to include

        Returns:
            Complete book analysis results
        """
        logger.info(f"Starting analysis of EPUB: {epub_path}")

        # Extract text from EPUB
        title, full_text = self.extract_text_from_epub(epub_path)

        # Extract key phrases using Azure
        key_phrases = self.extract_key_phrases_from_text(full_text)
        logger.info(f"Extracted {len(key_phrases)} key phrases from text")

        # Calculate frequencies of key phrases in the original text
        # (automatically filters to 2-4 character words with 3+ occurrences)
        word_frequencies = self.count_phrase_frequencies_in_text(key_phrases, full_text)

        # Calculate vocabulary statistics
        total_words = sum(word_frequencies.values())
        unique_words = len(word_frequencies)
        chinese_words = total_words  # All phrases are Chinese after key phrase extraction
        unique_chinese_words = unique_words

        stats = VocabularyStats(
            total_words=total_words,
            unique_words=unique_words,
            chinese_words=chinese_words,
            unique_chinese_words=unique_chinese_words,
        )

        # Calculate HSK distribution
        hsk_distribution = self.calculate_hsk_distribution(word_frequencies)

        # Compare with Anki collection
        known_words, unknown_words = self.compare_with_anki_collection(word_frequencies, anki_words)

        # Get high-frequency unknown words
        high_frequency_unknown = self.get_high_frequency_unknown_words(unknown_words, top_unknown_count)

        # Calculate coverage targets
        coverage_targets = self.calculate_coverage_targets(word_frequencies, known_words, target_coverages)

        # Identify non-HSK words
        non_hsk_words = self.identify_non_hsk_words(word_frequencies)

        # Calculate HSK learning targets
        hsk_learning_targets = self.calculate_hsk_learning_targets(word_frequencies, known_words)

        logger.info(
            f"Analysis complete: {unique_words} unique words, "
            f"{len(known_words)} known, {len(unknown_words)} unknown, "
            f"{len(non_hsk_words)} non-HSK"
        )

        return BookAnalysis(
            title=title,
            stats=stats,
            word_frequencies=word_frequencies,
            hsk_distribution=hsk_distribution,
            known_words=known_words,
            unknown_words=unknown_words,
            high_frequency_unknown=high_frequency_unknown,
            coverage_targets=coverage_targets,
            non_hsk_words=non_hsk_words,
            hsk_learning_targets=hsk_learning_targets,
        )
