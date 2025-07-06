"""Pleco-related models and functionality."""

from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterator
import re

from .anki import AnkiCard
from .chinese import convert_numbered_pinyin_to_tones, get_semantic_components
from .constants import (
    PARTS_OF_SPEECH, 
    PART_OF_SPEECH_ABBREVIATIONS,
    DOMAIN_MARKERS,
    COMPILED_PATTERNS,
    COMPILED_DOMAIN_PATTERNS,
    COMPILED_POS_PATTERNS,
    COMPILED_ABBREV_PATTERNS
)


@dataclass
class PlecoEntry:
    """Represents a single Pleco flashcard entry."""

    chinese: str
    pinyin: str
    definition: str

    def __str__(self) -> str:
        return f"{self.chinese} ({self.pinyin}): {self.definition}"


@dataclass
class PlecoCollection:
    """Represents a collection of Pleco flashcard entries."""

    entries: List[PlecoEntry]

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self) -> Iterator[PlecoEntry]:
        return iter(self.entries)

    def add_entry(self, entry: PlecoEntry) -> None:
        """Add a new entry to the collection."""
        self.entries.append(entry)


def _detect_parts_of_speech_positions(definition: str) -> List[Tuple[int, int, str]]:
    """Detect positions of parts of speech in definition, excluding those in parentheses."""
    pos_positions = []
    for pos in PARTS_OF_SPEECH:
        pattern = rf"\b{pos}\b"
        for match in re.finditer(pattern, definition, re.IGNORECASE):
            # Check if this match is inside parentheses
            start_pos = match.start()
            preceding_text = definition[:start_pos]
            following_text = definition[start_pos:]

            # Check if we're inside parentheses
            in_parentheses = False
            paren_depth = 0
            for char in preceding_text:
                if char == "(":
                    paren_depth += 1
                elif char == ")":
                    paren_depth -= 1

            # If paren_depth > 0, we're inside parentheses
            if paren_depth > 0:
                # Check if there's a closing parenthesis after this position
                if ")" in following_text:
                    in_parentheses = True

            # Only add to pos_positions if not in parentheses
            if not in_parentheses:
                pos_positions.append((match.start(), match.end(), pos))

    # Sort by position
    pos_positions.sort()
    return pos_positions


def _extract_meaning_sections(definition: str, pos_positions: List[Tuple[int, int, str]]) -> Tuple[List[str], List[str]]:
    """Extract meaning sections and examples from definition based on parts of speech positions."""
    meanings = []
    examples = []

    if not pos_positions:
        # No parts of speech found, treat as single meaning
        meaning, extracted_examples = extract_examples_from_text(definition)
        meanings.append(meaning)
        if extracted_examples:
            examples.extend(extracted_examples)
    else:
        # Process each meaning section
        for i, (start, _, pos) in enumerate(pos_positions):
            # Find the end of this meaning section
            if i + 1 < len(pos_positions):
                section_end = pos_positions[i + 1][0]
            else:
                section_end = len(definition)

            section_text = definition[start:section_end].strip()

            # Extract meaning and examples from this section
            meaning, extracted_examples = extract_examples_from_text(section_text)
            meanings.append(meaning)
            if extracted_examples:
                examples.extend(extracted_examples)

    return meanings, examples


def _format_meaning_with_html(meanings: List[str]) -> str:
    """Format meanings with HTML tags for parts of speech and domain markers."""
    combined_meaning = "\n".join(meanings)

    # Handle abbreviations first using pre-compiled patterns
    for pattern, replacement in COMPILED_ABBREV_PATTERNS.items():
        combined_meaning = pattern.sub(replacement, combined_meaning)

    # Handle idiom in parentheses - move "(idiom)" from end to beginning as "<b>idiom</b>"
    if "(idiom)" in combined_meaning.lower():
        combined_meaning = COMPILED_PATTERNS["idiom_parentheses"].sub("", combined_meaning)
        combined_meaning = "<b>idiom</b> " + combined_meaning.strip()

    # Handle subject/domain markers using pre-compiled patterns
    for pattern, display_text in COMPILED_DOMAIN_PATTERNS.items():
        replacement = f'<span color="red">{display_text}</span>'
        combined_meaning = pattern.sub(replacement, combined_meaning)

    # Handle full parts of speech using pre-compiled patterns
    for pos, pattern in COMPILED_POS_PATTERNS.items():
        combined_meaning = pattern.sub(f"<b>{pos}</b>", combined_meaning)

    return combined_meaning


def parse_pleco_definition(definition: str) -> Tuple[str, Optional[List[str]]]:
    """Parse Pleco definition to extract meanings and examples."""
    # Detect parts of speech positions 
    pos_positions = _detect_parts_of_speech_positions(definition)
    
    # Extract meaning sections and examples
    meanings, examples = _extract_meaning_sections(definition, pos_positions)
    
    # Format meanings with HTML
    formatted_meaning = _format_meaning_with_html(meanings)
    
    return formatted_meaning, examples if examples else None


def extract_examples_from_text(text: str) -> Tuple[str, Optional[List[str]]]:
    """Extract examples from a text section, returning cleaned meaning and examples."""

    # Handle abbreviation pattern using pre-compiled pattern
    abbrev_match = COMPILED_PATTERNS["abbreviation"].search(text)
    if abbrev_match:
        # Extract just the English translation at the end, but preserve any part of speech at the beginning
        english_part = abbrev_match.group(1).strip()

        # Check if the text starts with a part of speech
        parts_pattern = "|".join(PARTS_OF_SPEECH)
        pos_match = re.match(rf"^({parts_pattern})\s+", text, re.IGNORECASE)
        if pos_match:
            pos_word = pos_match.group(1)
            meaning = f"{pos_word} {english_part}"
        else:
            meaning = english_part

        return meaning, None

    # Find Chinese example sentences using multiple patterns
    chinese_examples = []
    
    # Pattern 1: Chinese sentence with punctuation + pinyin + English with punctuation
    pattern1 = r'[一-龯][^.。]*[.。]\s+[A-Za-z][^.]*?[.!?]\s*(?:[A-Z][^.]*?[.!?]\s*)*'
    examples1 = re.findall(pattern1, text)
    chinese_examples.extend(examples1)
    
    # Pattern 2: Any text starting with Chinese chars that goes to the end after the meaning
    # Look for Chinese chars followed by space and capitalized word, going to end of string
    remaining_text = text
    for found_example in chinese_examples:
        remaining_text = remaining_text.replace(found_example, '')
    
    # Now look for any remaining Chinese examples in the remaining text
    pattern2 = r'[一-龯][^$]*$'
    examples2 = re.findall(pattern2, remaining_text.strip())
    
    # Filter and add unique examples
    for ex in examples2:
        if ex.strip() and not any(ex.strip() in found for found in chinese_examples):
            chinese_examples.append(ex.strip())
    
    if chinese_examples:
        # Remove Chinese examples from text to get clean meaning
        meaning_text = text
        for example in chinese_examples:
            meaning_text = meaning_text.replace(example, ' ')
        
        # Clean up the meaning using pre-compiled pattern
        meaning = COMPILED_PATTERNS["whitespace_cleanup"].sub(" ", meaning_text).strip()
        examples = chinese_examples if chinese_examples else None
    else:
        # Fallback to original simple logic
        chinese_match = COMPILED_PATTERNS["chinese_chars"].search(text)
        if chinese_match:
            meaning = text[: chinese_match.start()].strip()
            examples_text = text[chinese_match.start() :].strip()
            examples = [examples_text] if examples_text else None
        else:
            meaning = text.strip()
            examples = None

    # Clean up extra spaces using pre-compiled pattern
    meaning = COMPILED_PATTERNS["whitespace_cleanup"].sub(" ", meaning).strip()

    return meaning, examples


def pleco_to_anki(pleco_entry: PlecoEntry) -> AnkiCard:
    """Convert a PlecoEntry to an AnkiCard."""
    meaning, examples = parse_pleco_definition(pleco_entry.definition)
    semantic_component = get_semantic_components(pleco_entry.chinese)

    return AnkiCard(
        pinyin=convert_numbered_pinyin_to_tones(pleco_entry.pinyin),
        simplified=pleco_entry.chinese,
        meaning=meaning,
        examples=examples,
        semantic_component=semantic_component,
        passive=True,
        nohearing=True,
    )
