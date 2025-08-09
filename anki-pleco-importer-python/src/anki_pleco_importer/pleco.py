"""Pleco-related models and functionality."""

from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterator
import re

from .anki import AnkiCard
from .chinese import convert_numbered_pinyin_to_tones, get_structural_decomposition_semantic
from .llm import FieldGenerator, FieldGenerationResult
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
        # Check if definition should be split by numbered meanings first
        numbered_sections = _split_by_numbered_meanings(definition)

        # Determine whether to use POS splitting or numbered splitting
        should_split_by_pos = len(pos_positions) > 1 and _should_split_by_pos(definition, pos_positions)

        if should_split_by_pos:
            # POS splitting takes precedence when there are clear POS boundaries
            # This handles cases like "noun 1 research 2 study verb 3 to research 4 to study"
            for i, (start, _, pos) in enumerate(pos_positions):
                # Find the end of this meaning section
                if i + 1 < len(pos_positions):
                    section_end = pos_positions[i + 1][0]
                else:
                    section_end = len(definition)

                section_text = definition[start:section_end].strip()

                # Check if this POS section has numbered subsections
                pos_numbered_sections = _split_by_numbered_meanings(section_text)
                if len(pos_numbered_sections) > 1:
                    # Process each numbered subsection within this POS
                    for numbered_section in pos_numbered_sections:
                        clean_section = re.sub(r"^\s*\d+\s+", "", numbered_section)
                        meaning, extracted_examples = extract_examples_from_text(clean_section)
                        meanings.append(meaning)
                        if extracted_examples:
                            examples.extend(extracted_examples)
                else:
                    # No numbered subsections, process as single meaning
                    meaning, extracted_examples = extract_examples_from_text(section_text)
                    meanings.append(meaning)
                    if extracted_examples:
                        examples.extend(extracted_examples)
        elif len(numbered_sections) > 1:
            # Use numbered sections when there's no clear POS boundary
            for numbered_section in numbered_sections:
                clean_section = re.sub(r"^\s*\d+\s+", "", numbered_section)
                meaning, extracted_examples = extract_examples_from_text(clean_section)
                meanings.append(meaning)
                if extracted_examples:
                    examples.extend(extracted_examples)
        else:
            # Treat as single meaning with inline POS markers
            meaning, extracted_examples = extract_examples_from_text(definition)
            meanings.append(meaning)
            if extracted_examples:
                examples.extend(extracted_examples)

    return meanings, examples


def _should_split_by_pos(definition: str, pos_positions: List[Tuple[int, int, str]]) -> bool:
    """Determine if definition should be split by POS positions based on strong structural indicators."""
    # Only split if there are very clear structural separators, not just semicolons
    # Semicolons are commonly used within single meanings to separate translations

    # Check for numbered patterns between POS markers
    for i in range(len(pos_positions) - 1):
        current_end = pos_positions[i][1]
        next_start = pos_positions[i + 1][0]
        between_text = definition[current_end:next_start].strip()

        # Split if there are numbers indicating separate definitions or clear separators
        if re.search(r"\d+\s+\w+", between_text) or " | " in between_text:
            return True

        # NEW: Also split if there's substantial content between different POS types
        # This handles cases like "verb ... examples ... noun ... examples"
        current_pos = pos_positions[i][2].lower()
        next_pos = pos_positions[i + 1][2].lower()

        # Case 1: Different POS types with substantial content and Chinese examples
        if current_pos != next_pos and len(between_text) > 50:
            # Check for Chinese text (examples) between the POS markers
            # This indicates separate definitions with their own examples
            if re.search(r"[一-龯]", between_text):
                return True

        # Case 2: Different POS types with numbered definitions
        # E.g. "noun 1 research 2 study verb 3 to research 4 to study"
        if current_pos != next_pos:
            # Check if the between_text contains numbered patterns
            # This suggests the POS markers are separating different numbered sections
            if re.search(r"\d+\s+[a-zA-Z]", between_text):
                return True

    return False


def _split_by_numbered_meanings(text: str) -> List[str]:
    """Split text by numbered meanings (1, 2, 3, etc.)."""
    # Pattern to match numbered meanings like "1 ", "2 ", "3 ", etc.
    # Include numbers at the start of string or preceded by whitespace
    # Make sure we don't match numbers inside Chinese text or other contexts
    # Allow letters, digits, or opening parenthesis to follow (for cases like "3D" and "2 (fig.)")
    pattern = r"(?:^|\s)(\d+)\s+(?=[a-zA-Z0-9(])"

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
    if not meanings:
        return ""

    # Check if first meaning is just a part-of-speech tag
    pos_patterns = [
        "noun",
        "verb",
        "adjective",
        "adverb",
        "pronoun",
        "preposition",
        "conjunction",
        "interjection",
        "idiom",
    ]

    result_parts = []

    # Process meanings, handling part-of-speech tags separately
    i = 0
    while i < len(meanings):
        current_meaning = meanings[i].strip()

        # Check if this is a standalone part-of-speech tag
        if current_meaning.lower() in pos_patterns:
            # Add the POS tag outside any list
            result_parts.append(f'<span class="part-of-speech">{current_meaning.lower()}</span>')
            i += 1

            # Collect subsequent meanings that belong to this POS
            pos_meanings = []
            while i < len(meanings) and meanings[i].strip().lower() not in pos_patterns:
                pos_meanings.append(meanings[i])
                i += 1

            # Format the meanings for this POS as a list if multiple, or single if one
            if len(pos_meanings) > 1:
                formatted_pos_meanings = []
                for meaning in pos_meanings:
                    formatted_meaning = _apply_semantic_markup_to_text(meaning)
                    formatted_pos_meanings.append(formatted_meaning)
                list_items = "</li><li>".join(formatted_pos_meanings)
                result_parts.append(f"<ol><li>{list_items}</li></ol>")
            elif len(pos_meanings) == 1:
                formatted_meaning = _apply_semantic_markup_to_text(pos_meanings[0])
                result_parts.append(formatted_meaning)
        else:
            # Not a standalone POS tag, treat as regular meaning
            formatted_meaning = _apply_semantic_markup_to_text(current_meaning)
            result_parts.append(formatted_meaning)
            i += 1

    # Check if we have multiple meanings but no POS tags were found
    # If result_parts equals the number of meanings, it means no POS processing occurred
    if len(result_parts) == len(meanings) and len(meanings) > 1:
        # No POS tags were detected but we have multiple meanings, format as ordered list
        formatted_meanings = []
        for meaning in meanings:
            formatted_meaning = _apply_semantic_markup_to_text(meaning)
            formatted_meanings.append(formatted_meaning)
        list_items = "</li><li>".join(formatted_meanings)
        return f"<ol><li>{list_items}</li></ol>"

    return " ".join(result_parts)


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
    # Pattern to match various formats:
    # 1. "Chinese (pinyin) - translation"
    # 2. "Chinese pinyin translation" (single words/phrases)
    # 3. "Chinese sentence. Pinyin sentence. English sentence."

    # First try pattern with parentheses and dash: "Chinese (pinyin) - translation"
    pattern1 = r"([一-龯]+)\s*\(([^)]+)\)\s*-\s*(.+)"
    match = re.search(pattern1, example)

    if match:
        hanzi = match.group(1).strip()
        pinyin = match.group(2).strip()
        translation = match.group(3).strip()

        return (
            f'<span class="hanzi">{hanzi}</span> '
            f'<span class="pinyin">{pinyin}</span> '
            f'<span class="translation">{translation}</span>'
        )

    # Second try pattern for sentences: "Chinese sentence. Pinyin sentence. English sentence."
    # Look for pattern with Chinese characters followed by punctuation, then pinyin, then English
    # Handle Chinese punctuation (。！？,) and English punctuation (.!?,)
    sentence_pattern = r"^([一-龯][^。！？]*[。！？,])\s+([A-ZĀ-ǜa-z][^.!?]*[.!?？])\s+(.+)$"
    match = re.search(sentence_pattern, example)

    if match:
        hanzi = match.group(1).strip()
        pinyin = match.group(2).strip()
        translation = match.group(3).strip()

        return (
            f'<span class="hanzi">{hanzi}</span> '
            f'<span class="pinyin">{pinyin}</span> '
            f'<span class="translation">{translation}</span>'
        )

    # Third try pattern: "Chinese phrase pinyin translation" (multi-character phrases without punctuation)
    # Use a more sophisticated approach to separate Chinese phrase, pinyin, and English
    # Pattern: Chinese characters followed by pinyin (with tone marks) followed by English
    phrase_pattern = r"^([一-龯][一-龯\s]*?[一-龯])\s+([a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ\s]+?)\s+([a-zA-Z][a-zA-Z\s]+?)$"
    match = re.search(phrase_pattern, example)
    if match:
        hanzi_candidate = match.group(1).strip()
        potential_pinyin = match.group(2).strip()
        potential_translation = match.group(3).strip()

        # Validate that the potential_pinyin contains tone marks or is recognizable pinyin
        # and the potential_translation looks like English (no tone marks)
        has_tone_marks = bool(re.search(r"[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]", potential_pinyin))
        is_english_translation = bool(re.search(r"[a-zA-Z]", potential_translation)) and not bool(
            re.search(r"[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]", potential_translation)
        )

        if has_tone_marks and is_english_translation:
            return (
                f'<span class="hanzi">{hanzi_candidate}</span> '
                f'<span class="pinyin">{potential_pinyin}</span> '
                f'<span class="translation">{potential_translation}</span>'
            )

    # Fourth try pattern without parentheses: "Chinese pinyin translation" (single words)
    # Split by spaces and find where Chinese ends and English begins
    parts = example.split()
    if len(parts) >= 3:
        # First part should be Chinese characters
        hanzi_candidate = parts[0]
        if re.match(r"^[一-龯]+$", hanzi_candidate):
            # Find where English starts (first word that looks like English, not pinyin)
            english_start_idx = None
            for i, part in enumerate(parts[1:], 1):
                # Check if this looks like English (contains English letters but no tone marks)
                if re.search(r"[a-zA-Z]", part) and not re.search(r"[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]", part):
                    english_start_idx = i
                    break

            if english_start_idx:
                hanzi = hanzi_candidate
                pinyin_parts = parts[1:english_start_idx]
                translation_parts = parts[english_start_idx:]

                pinyin = " ".join(pinyin_parts)
                translation = " ".join(translation_parts)

                return (
                    f'<span class="hanzi">{hanzi}</span> '
                    f'<span class="pinyin">{pinyin}</span> '
                    f'<span class="translation">{translation}</span>'
                )

    # If no pattern matches, return as-is
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


def find_existing_pronunciation(
    character: str, pinyin: str, anki_parser: Optional[AnkiExportParser] = None
) -> Optional[str]:
    """
    Find existing pronunciation for any character with exactly matching pinyin in Anki export.

    Args:
        character: Single Chinese character to search for (used for validation only)
        pinyin: Pinyin to match exactly
        anki_parser: AnkiExportParser instance with loaded cards

    Returns:
        Existing pronunciation filename if found, None otherwise
    """
    if not anki_parser or len(character) != 1:
        return None

    # Convert input pinyin to tones for consistent comparison
    target_pinyin = convert_numbered_pinyin_to_tones(pinyin)

    for card in anki_parser.cards:
        # Check if this card has matching pinyin and audio (ignoring the specific character)
        clean_chars = card.get_clean_characters()
        if len(clean_chars) == 1 and card.pinyin == target_pinyin and card.audio:  # Only match single-character cards
            return card.audio

    return None


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
            # Format: word pinyin meaning
            example = f"{clean_chars} {tone_pinyin} {card.definitions}"
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
        if card.notetype in ["Chinese", "Chinese 2"]:
            clean_chars = card.get_clean_characters()
            if clean_chars and len(clean_chars) <= 4:  # Limit to reasonable word lengths
                dictionary[clean_chars] = {
                    "pinyin": card.pinyin,
                    "definition": card.definitions,
                }

    return dictionary


def pleco_to_anki(
    pleco_entry: PlecoEntry,
    anki_export_parser: AnkiExportParser,
    field_generator: Optional[FieldGenerator] = None,
    pregenerated_result: Optional[FieldGenerationResult] = None,
) -> AnkiCard:
    """Convert a PlecoEntry to an AnkiCard, optionally enhanced with Anki export examples."""
    meaning, examples, similar_characters = parse_pleco_definition_semantic(pleco_entry.definition)

    anki_dictionary = _create_anki_dictionary(anki_export_parser)

    # Enhance similar characters with pinyin and definitions from Anki dictionary
    enhanced_similar_characters = None
    if similar_characters:
        enhanced_similar_characters = []
        for char in similar_characters:
            if char in anki_dictionary:
                # Format: character pinyin definition
                char_info = anki_dictionary[char]
                tone_pinyin = convert_numbered_pinyin_to_tones(char_info["pinyin"])
                enhanced_char = f"{char} {tone_pinyin} {char_info['definition']}"
                enhanced_similar_characters.append(enhanced_char)
            else:
                # Just the character if not found in dictionary
                enhanced_similar_characters.append(char)

    if pregenerated_result:
        structural_decomposition = pregenerated_result.structural_decomposition
        etymology = pregenerated_result.etymology
    elif field_generator:
        generated = field_generator.generate(pleco_entry.chinese, pleco_entry.pinyin)
        structural_decomposition = generated.structural_decomposition
        etymology = generated.etymology
    else:
        structural_decomposition = get_structural_decomposition_semantic(pleco_entry.chinese, anki_dictionary)
        etymology = None

    # Check for existing pronunciation for single characters
    existing_pronunciation = None
    skip_audio = False
    if len(pleco_entry.chinese) == 1 and anki_export_parser:
        # Look for existing pronunciation with exactly matching pinyin
        existing_pronunciation = find_existing_pronunciation(
            pleco_entry.chinese, pleco_entry.pinyin, anki_export_parser
        )
        if existing_pronunciation:
            skip_audio = True

        # Add multi-character examples from Anki export
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
        etymology=etymology,
        pronunciation=existing_pronunciation,
        passive=True,
        nohearing=skip_audio,
    )
