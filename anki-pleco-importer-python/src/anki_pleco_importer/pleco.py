"""Pleco-related models and functionality."""

from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterator
import re

from .anki import AnkiCard
from .chinese import convert_numbered_pinyin_to_tones, get_structural_decomposition
from .anki_parser import AnkiExportParser
from .constants import (
    PARTS_OF_SPEECH,
    COMPILED_PATTERNS,
    COMPILED_DOMAIN_PATTERNS,
    COMPILED_POS_PATTERNS,
    COMPILED_ABBREV_PATTERNS,
    COMPILED_SEMANTIC_POS_PATTERNS,
    COMPILED_SEMANTIC_ABBREV_PATTERNS,
    COMPILED_SEMANTIC_DOMAIN_PATTERNS,
    COMPILED_SEMANTIC_USAGE_PATTERNS,
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
    """Detect positions of parts of speech in definition, excluding parentheses."""
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


def _extract_meaning_sections(
    definition: str, pos_positions: List[Tuple[int, int, str]]
) -> Tuple[List[str], List[str]]:
    """Extract meaning sections and examples from definition based on POS positions."""
    meanings = []
    examples = []

    if not pos_positions:
        # No parts of speech found, but check for numbered meanings
        numbered_sections = _split_by_numbered_meanings(definition)

        if len(numbered_sections) > 1:
            # Process each numbered section separately
            for numbered_section in numbered_sections:
                # Remove the leading number from the meaning since it will be in a list
                clean_section = re.sub(r"^\s*\d+\s+", "", numbered_section)
                meaning, extracted_examples = extract_examples_from_text(clean_section)
                meanings.append(meaning)
                if extracted_examples:
                    examples.extend(extracted_examples)
        else:
            # Treat as single meaning
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

            # Check if this section contains numbered meanings (1, 2, 3, etc.)
            numbered_sections = _split_by_numbered_meanings(section_text)

            if len(numbered_sections) > 1:
                # Process each numbered section separately
                for numbered_section in numbered_sections:
                    # Remove the leading number from the meaning since it will be in a list
                    clean_section = re.sub(r"^\s*\d+\s+", "", numbered_section)
                    meaning, extracted_examples = extract_examples_from_text(clean_section)
                    meanings.append(meaning)
                    if extracted_examples:
                        examples.extend(extracted_examples)
            else:
                # Extract meaning and examples from this section
                meaning, extracted_examples = extract_examples_from_text(section_text)
                meanings.append(meaning)
                if extracted_examples:
                    examples.extend(extracted_examples)

    return meanings, examples


def _split_by_numbered_meanings(text: str) -> List[str]:
    """Split text by numbered meanings (1, 2, 3, etc.)."""
    # Pattern to match numbered meanings like "1 ", "2 ", "3 ", etc.
    # Make sure we don't match numbers inside Chinese text or other contexts
    pattern = r"\s+(\d+)\s+(?=[a-zA-Z])"

    # Find all numbered positions
    matches = list(re.finditer(pattern, text))

    if not matches:
        return [text]

    sections = []
    start = 0

    for match in matches:
        # Add section from start to current number
        if match.start() > start:
            sections.append(text[start : match.start()].strip())
        start = match.start()

    # Add the last section
    if start < len(text):
        sections.append(text[start:].strip())

    # Filter out empty sections
    return [section for section in sections if section.strip()]


def _format_meaning_with_html(meanings: List[str]) -> str:
    """Format meanings with HTML tags for parts of speech and domain markers."""
    combined_meaning = "\n".join(meanings)

    # Handle abbreviations first using pre-compiled patterns
    for pattern, replacement in COMPILED_ABBREV_PATTERNS.items():
        combined_meaning = pattern.sub(replacement, combined_meaning)

    # Handle idiom in parentheses - move "(idiom)" from end to beginning
    if "(idiom)" in combined_meaning.lower():
        combined_meaning = COMPILED_PATTERNS["idiom_parentheses"].sub("", combined_meaning)
        combined_meaning = "<b>idiom</b> " + combined_meaning.strip()

    # Handle subject/domain markers using pre-compiled patterns
    for pattern, display_text in COMPILED_DOMAIN_PATTERNS.items():
        replacement = f'<span style="color: red;">{display_text}</span>'
        combined_meaning = pattern.sub(replacement, combined_meaning)

    # Handle full parts of speech using pre-compiled patterns
    for pos, pattern in COMPILED_POS_PATTERNS.items():
        combined_meaning = pattern.sub(f"<b>{pos}</b>", combined_meaning)

    return combined_meaning


def _format_meaning_with_semantic_markup(meanings: List[str]) -> str:
    """Format meanings with semantic HTML classes and lists instead of inline styling."""
    # If there are multiple meanings, format as an ordered list
    if len(meanings) > 1:
        formatted_meanings = []
        for meaning in meanings:
            # Apply semantic markup to each meaning
            formatted_meaning = _apply_semantic_markup_to_text(meaning)
            formatted_meanings.append(formatted_meaning)
        list_items = "</li><li>".join(formatted_meanings)
        return f"<ol><li>{list_items}</li></ol>"

    # Single meaning - apply semantic markup directly
    if meanings:
        return _apply_semantic_markup_to_text(meanings[0])

    return ""


def _apply_semantic_markup_to_text(text: str) -> str:
    """Apply semantic markup patterns to a single text string."""
    # Handle abbreviations first using semantic patterns
    for pattern, replacement in COMPILED_SEMANTIC_ABBREV_PATTERNS.items():
        text = pattern.sub(replacement, text)

    # Handle idiom in parentheses - move "(idiom)" from end to beginning
    if "(idiom)" in text.lower():
        text = COMPILED_PATTERNS["idiom_parentheses"].sub("", text)
        text = '<span class="part-of-speech">idiom</span> ' + text.strip()

    # Handle usage markers first (before domain markers to avoid conflicts)
    for pattern, replacement in COMPILED_SEMANTIC_USAGE_PATTERNS.items():
        text = pattern.sub(replacement, text)

    # Handle domain markers using semantic patterns (excluding usage markers already handled)
    for pattern, replacement in COMPILED_SEMANTIC_DOMAIN_PATTERNS.items():
        # Skip if this is a usage marker that was already handled
        pattern_text = pattern.pattern.replace(r"\b", "").replace("\\b", "")
        usage_patterns = [
            p.pattern.replace(r"\b", "").replace("\\b", "") for p in COMPILED_SEMANTIC_USAGE_PATTERNS.keys()
        ]
        if pattern_text not in usage_patterns:
            text = pattern.sub(replacement, text)

    # Handle full parts of speech using semantic patterns
    for pos, pattern in COMPILED_SEMANTIC_POS_PATTERNS.items():
        text = pattern.sub(f'<span class="part-of-speech">{pos}</span>', text)

    return text


def parse_pleco_definition(definition: str) -> Tuple[str, Optional[List[str]], Optional[List[str]]]:
    """Parse Pleco definition to extract meanings, examples, and similar characters."""
    # Extract opposite patterns first and clean them from definition
    similar_characters = []

    # Find all opposite patterns
    opposite_matches = COMPILED_PATTERNS["opposite"].findall(definition)
    if opposite_matches:
        similar_characters.extend(opposite_matches)
        # Remove the opposite patterns from the definition
        definition = COMPILED_PATTERNS["opposite"].sub("", definition).strip()

    # Detect parts of speech positions
    pos_positions = _detect_parts_of_speech_positions(definition)

    # Extract meaning sections and examples
    meanings, examples = _extract_meaning_sections(definition, pos_positions)

    # Format meanings with HTML
    formatted_meaning = _format_meaning_with_html(meanings)

    return (formatted_meaning, examples if examples else None, similar_characters if similar_characters else None)


def parse_pleco_definition_semantic(definition: str) -> Tuple[str, Optional[List[str]], Optional[List[str]]]:
    """Parse Pleco definition with semantic markup instead of inline styling."""
    # Extract opposite patterns first and clean them from definition
    similar_characters = []

    # Find all opposite patterns
    opposite_matches = COMPILED_PATTERNS["opposite"].findall(definition)
    if opposite_matches:
        similar_characters.extend(opposite_matches)
        # Remove the opposite patterns from the definition
        definition = COMPILED_PATTERNS["opposite"].sub("", definition).strip()

    # Detect parts of speech positions
    pos_positions = _detect_parts_of_speech_positions(definition)

    # Extract meaning sections and examples
    meanings, examples = _extract_meaning_sections(definition, pos_positions)

    # Format meanings with semantic markup
    formatted_meaning = _format_meaning_with_semantic_markup(meanings)

    return (formatted_meaning, examples if examples else None, similar_characters if similar_characters else None)


def format_examples_with_semantic_markup(examples: Optional[List[str]]) -> Optional[str]:
    """Format examples as HTML list with semantic classes for hanzi, pinyin, and translation."""
    if not examples or len(examples) == 0:
        return None

    # Single example - just apply semantic markup
    if len(examples) == 1:
        return _format_single_example_semantic(examples[0])

    # Multiple examples - create unordered list
    formatted_examples = []
    for example in examples:
        formatted_example = _format_single_example_semantic(example)
        formatted_examples.append(formatted_example)

    list_items = '</li><li class="example">'.join(formatted_examples)
    return f'<ul><li class="example">{list_items}</li></ul>'


def _format_single_example_semantic(example: str) -> str:
    """Format a single example with semantic markup for hanzi, pinyin, and translation."""
    # Pattern to match: "Chinese (pinyin) - translation"

    # More flexible pattern to match Chinese characters followed by pinyin in parentheses
    pattern = r"([一-龯]+)\s*\(([^)]+)\)\s*-\s*(.+)"
    match = re.search(pattern, example)

    if match:
        hanzi = match.group(1).strip()
        pinyin = match.group(2).strip()
        translation = match.group(3).strip()

        return (
            f'<span class="hanzi">{hanzi}</span> '
            f'(<span class="pinyin">{pinyin}</span>) - '
            f'<span class="translation">{translation}</span>'
        )

    # If pattern doesn't match, return as-is
    return example


def extract_examples_from_text(text: str) -> Tuple[str, Optional[List[str]]]:
    """Extract examples from a text section, returning cleaned meaning and examples."""

    # Handle abbreviation pattern using pre-compiled pattern
    abbrev_match = COMPILED_PATTERNS["abbreviation"].search(text)
    if abbrev_match:
        # Extract just the English translation at the end, but preserve any POS
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

    # Extract examples using a systematic approach
    examples = []

    # First, find the start of Chinese content
    chinese_match = COMPILED_PATTERNS["chinese_chars"].search(text)
    if not chinese_match:
        # No Chinese characters found, return the whole text as meaning
        return text.strip(), None

    # Split text into meaning part and examples part
    meaning_part = text[: chinese_match.start()].strip()
    examples_part = text[chinese_match.start() :].strip()

    # Handle multiple examples separated by semicolons
    if " ; " in examples_part:
        # Split by semicolon and process each part
        parts = examples_part.split(" ; ")
        for part in parts:
            part = part.strip()
            if part and re.search(r"[一-龯]", part):
                examples.append(part)
    else:
        # Single example or complex pattern
        # Look for patterns like "Chinese pinyin English" or "Chinese. pinyin English."

        # Try to find multiple examples within the text
        # Look for patterns where Chinese text is followed by pinyin and English

        # Strategy: Split the text by looking for Chinese characters that mark examples
        # Pattern: Chinese chars followed by space and lowercase (pinyin) or uppercase

        # First, try to split by looking for Chinese words/phrases that start examples
        # Use a more sophisticated approach to find example boundaries

        # Look for positions where Chinese characters appear after English text
        # This suggests the start of a new example
        chinese_positions = []
        for match in re.finditer(r"[一-龯]+", examples_part):
            chinese_positions.append(match.start())

        if len(chinese_positions) > 1:
            # Multiple Chinese segments found - try to split into individual examples
            # Use a simple approach: look for clear boundaries

            # Try a different strategy: look for examples that end with patterns
            # Pattern for the first type: Chinese + pinyin + English words ending before
            # Pattern for the second type: Chinese sentence with punctuation + pinyin

            # Strategy: Look for positions where we have a clear break
            # A break is defined as: English text followed by space and then Chinese
            break_positions = []

            # Look for pattern: English word/punctuation + space + Chinese characters
            for match in re.finditer(r"[a-zA-Z.!?]\s+[一-龯]", examples_part):
                break_positions.append(match.end() - 1)  # Position of the Chinese character

            # Now split based on these break positions
            if break_positions:
                # Add start and end positions
                all_positions = [0] + break_positions + [len(examples_part)]

                for i in range(len(all_positions) - 1):
                    start = all_positions[i]
                    end = all_positions[i + 1]
                    example = examples_part[start:end].strip()
                    if example:
                        examples.append(example)
            else:
                # No clear breaks found, split by Chinese positions as before
                for i, pos in enumerate(chinese_positions):
                    if i + 1 < len(chinese_positions):
                        example = examples_part[pos : chinese_positions[i + 1]].strip()
                    else:
                        example = examples_part[pos:].strip()

                    if example:
                        examples.append(example)

        # If pattern didn't find multiple examples, try the structured approach
        if not examples:
            # Pattern 1: Chinese sentence/phrase followed by pinyin and English
            # This pattern should capture the full English translation
            pattern1 = r"[一-龯][^.。;]*[.。]?\s+[A-Z][a-z]*(?:\s+[a-z]+)*[^.]*?[.!?]" r"(?:\s+[A-Z][^.]*?[.!?])*(?:\s|$)"
            matches1 = re.findall(pattern1, examples_part)

            if matches1:
                # Found structured examples - clean them up
                for match_str in matches1:
                    match_text = match_str.strip()
                    if match_text:
                        examples.append(match_text)
            else:
                # Pattern 2: Look for Chinese phrases without full sentence structure
                # This handles cases like "履行合同 lǚxíng hétong fulfill a contract"
                pattern2 = r"[一-龯]+[^;]*?[a-z]+(?:\s+[a-z]+)*[^;]*?(?=\s+[一-龯]|$)"
                matches2 = re.findall(pattern2, examples_part)

                if matches2:
                    examples.extend([match.strip() for match in matches2])
                else:
                    # Fallback: treat the entire examples_part as one example
                    examples = [examples_part]

    # Clean up examples
    if examples:
        cleaned_examples = []
        for example in examples:
            # Remove any leading/trailing whitespace
            example = example.strip()
            # Remove any trailing semicolons or separators
            example = re.sub(r"[;\s]+$", "", example)
            if example:
                cleaned_examples.append(example)
        examples = cleaned_examples

    # Clean up meaning part
    meaning = meaning_part
    # Remove any trailing semicolons or separators
    meaning = re.sub(r"[;\s]+$", "", meaning).strip()

    return meaning, examples if examples else None


def find_multi_character_words_containing(character: str, anki_parser: Optional[AnkiExportParser] = None) -> List[str]:
    """
    Find multi-character words containing the given character from Anki export.

    Args:
        character: Single Chinese character to search for
        anki_parser: AnkiExportParser instance with loaded cards

    Returns:
        List of formatted examples like "学习 (xuéxí) - to learn, to study"
    """
    if not anki_parser or len(character) != 1:
        return []

    examples = []
    for card in anki_parser.cards:
        clean_chars = card.get_clean_characters()
        # Only include multi-character words that contain our character
        if len(clean_chars) > 1 and character in clean_chars:
            # Convert pinyin from numbered format to tone marks
            tone_pinyin = convert_numbered_pinyin_to_tones(card.pinyin)
            # Format: word (pinyin) - meaning
            example = f"{clean_chars} ({tone_pinyin}) - {card.definitions}"
            examples.append(example)

    # Limit to top 10 examples to avoid overwhelming the card
    return examples[:10]


def _create_anki_dictionary(anki_parser: AnkiExportParser) -> dict:
    """
    Create a dictionary from Anki export for structural decomposition.

    Args:
        anki_parser: AnkiExportParser instance with loaded cards

    Returns:
        Dictionary mapping Chinese words to their pinyin and definitions
    """
    dictionary = {}

    for card in anki_parser.cards:
        if card.notetype == "Chinese":
            clean_chars = card.get_clean_characters()
            if clean_chars and len(clean_chars) <= 4:  # Limit to reasonable word lengths
                dictionary[clean_chars] = {
                    "pinyin": card.pinyin,
                    "definition": card.definitions,
                }

    return dictionary


def pleco_to_anki(pleco_entry: PlecoEntry, anki_export_parser: AnkiExportParser) -> AnkiCard:
    """
    Convert a PlecoEntry to an AnkiCard, optionally enhanced with Anki export examples.
    """
    meaning, examples, similar_characters = parse_pleco_definition(pleco_entry.definition)

    anki_dictionary = _create_anki_dictionary(anki_export_parser)

    # Enhance similar characters with pinyin and definitions from Anki dictionary
    enhanced_similar_characters = None
    if similar_characters:
        enhanced_similar_characters = []
        for char in similar_characters:
            if char in anki_dictionary:
                # Format: character (pinyin) - definition
                char_info = anki_dictionary[char]
                tone_pinyin = convert_numbered_pinyin_to_tones(char_info["pinyin"])
                enhanced_char = f"{char} ({tone_pinyin}) - {char_info['definition']}"
                enhanced_similar_characters.append(enhanced_char)
            else:
                # Just the character if not found in dictionary
                enhanced_similar_characters.append(char)

    structural_decomposition = get_structural_decomposition(pleco_entry.chinese, anki_dictionary)

    # For single character words, add multi-character examples from Anki export
    if len(pleco_entry.chinese) == 1 and anki_export_parser:
        multi_char_examples = find_multi_character_words_containing(pleco_entry.chinese, anki_export_parser)
        # Add multi-character examples to existing examples
        if multi_char_examples:
            examples = (examples or []) + multi_char_examples

    return AnkiCard(
        pinyin=convert_numbered_pinyin_to_tones(pleco_entry.pinyin),
        simplified=pleco_entry.chinese,
        meaning=meaning,
        examples=examples,
        similar_characters=enhanced_similar_characters,
        structural_decomposition=structural_decomposition,
        passive=True,
        nohearing=True,
    )
