"""Parser for Anki export format."""

import re
from dataclasses import dataclass
from typing import List, Dict, Set, Optional, NamedTuple
from pathlib import Path
import pypinyin


class CandidateCharacter(NamedTuple):
    """Represents a candidate character with its analysis data."""

    character: str
    score: int
    word_count: int
    pinyin: str
    hsk_level: Optional[int] = None


@dataclass
class AnkiCard:
    """Represents a single Anki card."""

    notetype: str
    pinyin: str
    characters: str
    audio: str
    definitions: str
    components: str = ""
    radicals: str = ""
    tags: str = ""
    _original_parts: Optional[List[str]] = None

    def get_clean_characters(self) -> str:
        """Extract clean Chinese characters without HTML tags."""
        if not self.characters:
            return ""
        # Remove HTML tags
        clean = re.sub(r"<[^>]+>", "", self.characters)
        return clean.strip()


class AnkiExportParser:
    """Parser for Anki export files."""

    def __init__(self) -> None:
        self.cards: List[AnkiCard] = []
        self.separator = "\t"
        self.html_mode = False

    def parse_file(self, file_path: Path) -> List[AnkiCard]:
        """Parse an Anki export file and return list of cards."""
        self.cards = []

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Handle header lines
                if line.startswith("#"):
                    self._parse_header(line)
                    continue

                # Parse card data
                parts = line.split(self.separator)
                if len(parts) >= 5:  # Minimum required fields
                    card = AnkiCard(
                        notetype=parts[0] if len(parts) > 0 else "",
                        pinyin=parts[1] if len(parts) > 1 else "",
                        characters=parts[2] if len(parts) > 2 else "",
                        audio=parts[3] if len(parts) > 3 else "",
                        definitions=parts[4] if len(parts) > 4 else "",
                        components=parts[7] if len(parts) > 7 else "",
                        radicals=parts[6] if len(parts) > 6 else "",
                        tags=parts[16] if len(parts) > 16 else "",
                    )
                    self.cards.append(card)

        return self.cards

    def _parse_header(self, line: str) -> None:
        """Parse header lines to extract format information."""
        if line.startswith("#separator:"):
            sep_name = line.split(":")[1]
            if sep_name == "tab":
                self.separator = "\t"
            elif sep_name == "comma":
                self.separator = ","
        elif line.startswith("#html:"):
            self.html_mode = line.split(":")[1].lower() == "true"

    def get_all_characters(self) -> Set[str]:
        """Get all unique Chinese characters from the cards."""
        characters = set()
        for card in self.cards:
            clean_chars = card.get_clean_characters()
            for char in clean_chars:
                if self._is_chinese_character(char):
                    characters.add(char)
        return characters

    def get_character_frequency(self) -> Dict[str, int]:
        """Get frequency count of each character across all cards."""
        freq: Dict[str, int] = {}
        for card in self.cards:
            clean_chars = card.get_clean_characters()
            for char in clean_chars:
                if self._is_chinese_character(char):
                    freq[char] = freq.get(char, 0) + 1
        return freq

    def get_single_character_words(self) -> Set[str]:
        """Get all single-character words (individual characters that are words)."""
        single_chars = set()
        for card in self.cards:
            clean_chars = card.get_clean_characters()
            if len(clean_chars) == 1 and self._is_chinese_character(clean_chars):
                single_chars.add(clean_chars)
        return single_chars

    def get_multi_character_words(self) -> List[str]:
        """Get all multi-character words."""
        multi_chars = []
        for card in self.cards:
            clean_chars = card.get_clean_characters()
            if len(clean_chars) > 1 and all(self._is_chinese_character(c) for c in clean_chars):
                multi_chars.append(clean_chars)
        return multi_chars

    def get_component_characters(self) -> Set[str]:
        """Extract characters mentioned as components/radicals."""
        components = set()
        for card in self.cards:
            # Look for characters in components and radicals fields
            for field in [card.components, card.radicals]:
                if field:
                    # Extract characters from component descriptions
                    # Look for patterns like 女(woman), 子(child), etc.
                    matches = re.findall(r"([一-龯])", field)
                    for match in matches:
                        if self._is_chinese_character(match):
                            components.add(match)
        return components

    def _is_chinese_character(self, char: str) -> bool:
        """Check if a character is a Chinese character."""
        return "\u4e00" <= char <= "\u9fff"

    def get_character_pinyin(self, character: str) -> Optional[str]:
        """
        Get the most common pinyin for a character by finding it in single-character words.
        If not found as single character, use hanzipy to get the pinyin.
        """
        if len(character) != 1:
            return None

        # First try to find it as a single-character word
        for card in self.cards:
            clean_chars = card.get_clean_characters()
            if clean_chars == character:
                return card.pinyin

        # If not found as single character, use pypinyin to get the pinyin
        try:
            pinyin_result = pypinyin.pinyin(character, style=pypinyin.TONE)
            if pinyin_result and len(pinyin_result) > 0 and len(pinyin_result[0]) > 0:
                return pinyin_result[0][0]
        except Exception:
            pass

        return None

    def analyze_candidate_characters(
        self, hsk_char_mapping: Optional[Dict[str, int]] = None
    ) -> List[CandidateCharacter]:
        """
        Find candidate characters to learn based on:
        1. HSK level (lower levels prioritized)
        2. Characters that appear in many multi-character words
        3. Characters that are components in other characters
        4. Characters that are NOT already single-character words

        Args:
            hsk_char_mapping: Optional mapping of characters to HSK levels
        """
        single_chars = self.get_single_character_words()
        multi_words = self.get_multi_character_words()
        component_chars = self.get_component_characters()

        # Count frequency in multi-character words
        multi_char_freq: Dict[str, int] = {}
        for word in multi_words:
            for char in word:
                if char not in single_chars:  # Only count if not already a single word
                    multi_char_freq[char] = multi_char_freq.get(char, 0) + 1

        # Calculate scores for candidate characters
        candidates: List[CandidateCharacter] = []
        for char in multi_char_freq:
            # Get HSK level for this character
            hsk_level = hsk_char_mapping.get(char) if hsk_char_mapping else None

            # Start with base frequency score
            base_score = multi_char_freq[char]

            # Give extra weight if it's a component character
            if char in component_chars:
                base_score += 10  # Heavy weight for component characters

            # Get pinyin for the character
            pinyin = self.get_character_pinyin(char) or "?"

            candidates.append(
                CandidateCharacter(
                    character=char,
                    score=base_score,
                    word_count=multi_char_freq[char],
                    pinyin=pinyin,
                    hsk_level=hsk_level,
                )
            )

        # Sort by score first (higher scores first), then by HSK level (lower levels first)
        def sort_key(candidate: CandidateCharacter) -> tuple:
            # Higher scores are better, so negate for ascending sort
            score_priority = -candidate.score
            # HSK level priority: None (no HSK) = 999, actual levels = their value
            hsk_priority = candidate.hsk_level if candidate.hsk_level is not None else 999
            return (score_priority, hsk_priority)

        candidates.sort(key=sort_key)

        return candidates
