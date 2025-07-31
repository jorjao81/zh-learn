"""HSK word list parsing and analysis functionality."""

from pathlib import Path
from typing import Dict, List, Set, NamedTuple, Optional
import logging

logger = logging.getLogger(__name__)


class HSKAnalysis(NamedTuple):
    """Results of HSK word analysis."""

    level: int
    total_words: int
    present_words: List[str]
    missing_words: List[str]
    coverage_percentage: float


class HSKWordLists:
    """Parser and manager for HSK word lists."""

    def __init__(self, hsk_dir: Optional[Path] = None):
        """
        Initialize HSK word lists parser.

        Args:
            hsk_dir: Directory containing HSK files. Defaults to current directory.
        """
        self.hsk_dir = hsk_dir or Path(".")
        self.word_lists: Dict[int, Set[str]] = {}
        self._load_word_lists()

    def _load_word_lists(self) -> None:
        """Load HSK word lists from files."""
        # HSK levels 1-6 are in separate files
        for level in range(1, 7):
            hsk_file = self.hsk_dir / f"HSK{level}.txt"
            if hsk_file.exists():
                self.word_lists[level] = self._load_word_list(hsk_file)
                logger.info(f"Loaded {len(self.word_lists[level])} words for HSK {level}")
            else:
                logger.warning(f"HSK{level}.txt not found in {self.hsk_dir}")

        # HSK levels 7-9 are in a combined file
        hsk_79_file = self.hsk_dir / "HSK7-9.txt"
        if hsk_79_file.exists():
            words_79 = self._load_word_list(hsk_79_file)
            # For simplicity, we'll treat HSK 7-9 as level 7
            self.word_lists[7] = words_79
            logger.info(f"Loaded {len(words_79)} words for HSK 7-9")
        else:
            logger.warning(f"HSK7-9.txt not found in {self.hsk_dir}")

    def _load_word_list(self, file_path: Path) -> Set[str]:
        """
        Load words from a single HSK file.

        Args:
            file_path: Path to the HSK word list file

        Returns:
            Set of Chinese words
        """
        words = set()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip()
                    if word:  # Skip empty lines
                        words.add(word)
        except Exception as e:
            logger.error(f"Failed to load HSK word list from {file_path}: {e}")

        return words

    def get_available_levels(self) -> List[int]:
        """Get list of available HSK levels."""
        return sorted(self.word_lists.keys())

    def get_words_for_level(self, level: int) -> Set[str]:
        """
        Get all words for a specific HSK level.

        Args:
            level: HSK level (1-7, where 7 represents HSK 7-9)

        Returns:
            Set of Chinese words for that level
        """
        return self.word_lists.get(level, set())

    def analyze_coverage(self, anki_words: Set[str], level: int) -> HSKAnalysis:
        """
        Analyze HSK word coverage for a specific level.

        Args:
            anki_words: Set of words present in Anki collection
            level: HSK level to analyze

        Returns:
            HSKAnalysis with coverage statistics
        """
        hsk_words = self.get_words_for_level(level)
        if not hsk_words:
            return HSKAnalysis(
                level=level,
                total_words=0,
                present_words=[],
                missing_words=[],
                coverage_percentage=0.0,
            )

        # Find which HSK words are present in Anki collection
        present_words = list(hsk_words.intersection(anki_words))
        missing_words = list(hsk_words - anki_words)

        # Calculate coverage percentage
        coverage_percentage = (len(present_words) / len(hsk_words)) * 100

        return HSKAnalysis(
            level=level,
            total_words=len(hsk_words),
            present_words=sorted(present_words),
            missing_words=sorted(missing_words),
            coverage_percentage=coverage_percentage,
        )

    def analyze_all_levels(self, anki_words: Set[str]) -> List[HSKAnalysis]:
        """
        Analyze HSK word coverage for all available levels.

        Args:
            anki_words: Set of words present in Anki collection

        Returns:
            List of HSKAnalysis for each level
        """
        analyses = []
        for level in self.get_available_levels():
            analysis = self.analyze_coverage(anki_words, level)
            analyses.append(analysis)

        return analyses

    def get_cumulative_coverage(self, anki_words: Set[str], up_to_level: int) -> HSKAnalysis:
        """
        Get cumulative HSK coverage from level 1 up to specified level.

        Args:
            anki_words: Set of words present in Anki collection
            up_to_level: Highest HSK level to include (inclusive)

        Returns:
            HSKAnalysis with cumulative statistics
        """
        all_hsk_words = set()

        # Combine words from level 1 up to specified level
        for level in range(1, up_to_level + 1):
            level_words = self.get_words_for_level(level)
            all_hsk_words.update(level_words)

        if not all_hsk_words:
            return HSKAnalysis(
                level=up_to_level,
                total_words=0,
                present_words=[],
                missing_words=[],
                coverage_percentage=0.0,
            )

        # Find which HSK words are present in Anki collection
        present_words = list(all_hsk_words.intersection(anki_words))
        missing_words = list(all_hsk_words - anki_words)

        # Calculate coverage percentage
        coverage_percentage = (len(present_words) / len(all_hsk_words)) * 100

        return HSKAnalysis(
            level=up_to_level,
            total_words=len(all_hsk_words),
            present_words=sorted(present_words),
            missing_words=sorted(missing_words),
            coverage_percentage=coverage_percentage,
        )

    def get_character_hsk_level(self, character: str) -> Optional[int]:
        """
        Get the HSK level for a given character based on the words it appears in.

        Args:
            character: Single Chinese character to look up

        Returns:
            Lowest HSK level where this character appears, or None if not found
        """
        if len(character) != 1:
            return None

        # Check each HSK level from lowest to highest
        for level in sorted(self.get_available_levels()):
            level_words = self.get_words_for_level(level)
            # Check if character appears in any word at this level
            for word in level_words:
                if character in word:
                    return level

        return None

    def create_character_hsk_mapping(self) -> Dict[str, int]:
        """
        Create a mapping of characters to their lowest HSK level.

        Returns:
            Dictionary mapping characters to HSK levels
        """
        char_to_level: Dict[str, int] = {}

        # Process levels from lowest to highest so we keep the lowest level
        for level in sorted(self.get_available_levels()):
            level_words = self.get_words_for_level(level)
            for word in level_words:
                for char in word:
                    # Only set if not already mapped (to keep lowest level)
                    if char not in char_to_level:
                        char_to_level[char] = level

        return char_to_level
