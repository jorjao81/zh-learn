"""EPUB Chinese vocabulary analysis functionality."""

import re
import logging
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
    import jieba

    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

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

    def __init__(self, hsk_word_lists: Optional[HSKWordLists] = None, custom_dict_path: Optional[Path] = None):
        """
        Initialize the EPUB analyzer.

        Args:
            hsk_word_lists: HSK word lists for level analysis
            custom_dict_path: Optional path to custom dictionary for domain-specific terms
        """
        if not EBOOKLIB_AVAILABLE:
            raise ImportError("ebooklib is required for EPUB analysis. " "Install it with: pip install ebooklib")

        if not JIEBA_AVAILABLE:
            raise ImportError("jieba is required for Chinese text segmentation. " "Install it with: pip install jieba")

        self.hsk_word_lists = hsk_word_lists or HSKWordLists()
        self.chinese_pattern = re.compile(r"[\u4e00-\u9fff]+")

        # Configure jieba for absolute highest quality settings
        jieba.setLogLevel(logging.WARNING)

        # Enable Paddle mode for best accuracy if available
        try:
            import paddle  # noqa: F401

            jieba.enable_paddle()
            logger.info("Enabled jieba Paddle mode for highest accuracy")
        except ImportError:
            logger.info("Paddle not available, using jieba HMM mode")

        # Initialize jieba tokenizer
        jieba.dt.check_initialized()

        # Load custom dictionary if provided for domain-specific terms
        if custom_dict_path and custom_dict_path.exists():
            logger.info(f"Loading custom dictionary: {custom_dict_path}")
            jieba.load_userdict(str(custom_dict_path))
            logger.info("Custom dictionary loaded successfully")

        # Force jieba to finish initialization for best performance
        jieba.initialize()

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

    def segment_chinese_text(self, text: str, min_length: int = 1) -> List[str]:
        """
        Segment Chinese text into words using jieba.

        Args:
            text: Input Chinese text
            min_length: Minimum word length to include

        Returns:
            List of segmented Chinese words
        """
        # Extract Chinese characters only
        chinese_text = "".join(self.chinese_pattern.findall(text))

        if not chinese_text:
            return []

        # Segment using jieba with absolute highest quality settings
        # cut_all=False: Use precise mode (not full mode)
        # HMM=True: Enable HMM for new word recognition
        words = jieba.cut(chinese_text, cut_all=False, HMM=True)

        # Convert generator to list for processing
        words = list(words)

        # Filter words: Chinese characters only, minimum length
        filtered_words = []

        for word in words:
            word = word.strip()
            if len(word) >= min_length and self.chinese_pattern.match(word) and len(word) > 0:
                filtered_words.append(word)

        return filtered_words

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
        self, word_frequencies: Dict[str, int], known_words: Set[str], targets: List[int] = [80, 90, 95, 98]
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
        Get the most frequent unknown words.

        Args:
            unknown_words: Dictionary of unknown words with frequencies
            count: Number of words to return

        Returns:
            List of (word, frequency, pinyin, hsk_level) tuples sorted by frequency
        """
        sorted_words = sorted(unknown_words.items(), key=lambda x: x[1], reverse=True)[:count]
        return [(word, freq, self.get_word_pinyin(word), self.get_word_hsk_level(word)) for word, freq in sorted_words]

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

            # Sort by frequency (descending)
            unknown_at_level.sort(key=lambda x: x[1], reverse=True)

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

        # Segment Chinese text
        words = self.segment_chinese_text(full_text)
        logger.info(f"Segmented {len(words)} words from text")

        # Calculate word frequencies
        word_frequencies = self.analyze_vocabulary_frequency(words)

        # Filter by minimum frequency
        if min_frequency > 1:
            word_frequencies = {word: freq for word, freq in word_frequencies.items() if freq >= min_frequency}

        # Calculate vocabulary statistics
        total_words = sum(word_frequencies.values())
        unique_words = len(word_frequencies)
        chinese_words = total_words  # All words are Chinese after segmentation
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
