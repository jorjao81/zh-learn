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
    COMPILED_ABBREV_PATTERNS,
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


def _extract_meaning_sections(
    definition: str, pos_positions: List[Tuple[int, int, str]]
) -> Tuple[List[str], List[str]]:
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

            # Check if this section contains numbered meanings (1, 2, 3, etc.)
            numbered_sections = _split_by_numbered_meanings(section_text)
            
            if len(numbered_sections) > 1:
                # Process each numbered section separately
                for numbered_section in numbered_sections:
                    meaning, extracted_examples = extract_examples_from_text(numbered_section)
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
    pattern = r'\s+(\d+)\s+(?=[a-zA-Z])'
    
    # Find all numbered positions
    matches = list(re.finditer(pattern, text))
    
    if not matches:
        return [text]
    
    sections = []
    start = 0
    
    for match in matches:
        # Add section from start to current number
        if match.start() > start:
            sections.append(text[start:match.start()].strip())
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

    # Extract examples using a systematic approach
    examples = []
    
    # First, find the start of Chinese content
    chinese_match = COMPILED_PATTERNS["chinese_chars"].search(text)
    if not chinese_match:
        # No Chinese characters found, return the whole text as meaning
        return text.strip(), None
    
    # Split text into meaning part and examples part
    meaning_part = text[:chinese_match.start()].strip()
    examples_part = text[chinese_match.start():].strip()
    
    # Handle multiple examples separated by semicolons
    if ' ; ' in examples_part:
        # Split by semicolon and process each part
        parts = examples_part.split(' ; ')
        for part in parts:
            part = part.strip()
            if part and re.search(r'[一-龯]', part):
                examples.append(part)
    else:
        # Single example or complex pattern
        # Look for patterns like "Chinese pinyin English" or "Chinese. pinyin English."
        
        # Try to find multiple examples within the text
        # Look for patterns where Chinese text is followed by pinyin and English translation
        
        # Strategy: Split the text by looking for Chinese characters that mark the start of a new example
        # Pattern: Chinese chars followed by space and lowercase letters (pinyin) or uppercase letters (English)
        
        # First, try to split by looking for Chinese words/phrases that start new examples
        # Use a more sophisticated approach to find example boundaries
        
        # Look for positions where Chinese characters appear after English text
        # This suggests the start of a new example
        chinese_positions = []
        for match in re.finditer(r'[一-龯]+', examples_part):
            chinese_positions.append(match.start())
        
        if len(chinese_positions) > 1:
            # Multiple Chinese segments found - try to split into individual examples
            # Use a simple approach: look for clear boundaries
            
            # Try a different strategy: look for examples that end with specific English patterns
            # Pattern for the first type: Chinese + pinyin + English words ending before next Chinese
            # Pattern for the second type: Chinese sentence with punctuation + pinyin + English sentence
            
            # Strategy: Look for positions where we have a clear break
            # A break is defined as: English text followed by space and then Chinese characters
            break_positions = []
            
            # Look for pattern: English word/punctuation + space + Chinese characters
            for match in re.finditer(r'[a-zA-Z.!?]\s+[一-龯]', examples_part):
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
                        example = examples_part[pos:chinese_positions[i + 1]].strip()
                    else:
                        example = examples_part[pos:].strip()
                    
                    if example:
                        examples.append(example)
        
        # If pattern didn't find multiple examples, try the structured approach
        if not examples:
            # Pattern 1: Chinese sentence/phrase followed by pinyin and English, possibly ending with punctuation
            # This pattern should capture the full English translation including multiple sentences
            pattern1 = r'[一-龯][^.。;]*[.。]?\s+[A-Z][a-z]*(?:\s+[a-z]+)*[^.]*?[.!?](?:\s+[A-Z][^.]*?[.!?])*(?:\s|$)'
            matches1 = re.findall(pattern1, examples_part)
            
            if matches1:
                # Found structured examples - clean them up
                for match in matches1:
                    match = match.strip()
                    if match:
                        examples.append(match)
            else:
                # Pattern 2: Look for Chinese phrases without full sentence structure
                # This handles cases like "履行合同 lǚxíng hétong fulfill a contract"
                pattern2 = r'[一-龯]+[^;]*?[a-z]+(?:\s+[a-z]+)*[^;]*?(?=\s+[一-龯]|$)'
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
            example = re.sub(r'[;\s]+$', '', example)
            if example:
                cleaned_examples.append(example)
        examples = cleaned_examples
    
    # Clean up meaning part
    meaning = meaning_part
    # Remove any trailing semicolons or separators
    meaning = re.sub(r'[;\s]+$', '', meaning).strip()
    
    return meaning, examples if examples else None


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
