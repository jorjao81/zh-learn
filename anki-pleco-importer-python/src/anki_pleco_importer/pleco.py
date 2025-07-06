"""Pleco-related models and functionality."""

from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterator
import re

from .anki import AnkiCard
from .chinese import convert_numbered_pinyin_to_tones, get_semantic_components


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


def parse_pleco_definition(definition: str) -> Tuple[str, Optional[List[str]]]:
    """Parse Pleco definition to extract meanings and examples."""
    parts_of_speech = [
        "verb",
        "noun",
        "adjective",
        "adverb",
        "pronoun",
        "preposition",
        "conjunction",
        "interjection",
        "idiom",
    ]

    # Find all parts of speech positions, but exclude those in parentheses
    pos_positions = []
    for pos in parts_of_speech:
        pattern = rf"\b{pos}\b"
        for match in re.finditer(pattern, definition, re.IGNORECASE):
            # Check if this match is inside parentheses
            start_pos = match.start()
            # Find the closest opening parenthesis before this position
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

    # Split definition into meaning sections
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

    # Format parts of speech with HTML
    combined_meaning = "\n".join(meanings)

    # Handle abbreviations first
    abbreviations = {
        r"\bV\.\s*": "<b>verb</b> ",
        r"\bN\.\s*": "<b>noun</b> ",
        r"\bAdj\.\s*": "<b>adjective</b> ",
        r"\bAdv\.\s*": "<b>adverb</b> ",
    }

    for abbrev_pattern, replacement in abbreviations.items():
        combined_meaning = re.sub(abbrev_pattern, replacement, combined_meaning, flags=re.IGNORECASE)

    # Handle idiom in parentheses - move "(idiom)" from end to beginning as "<b>idiom</b>"
    if "(idiom)" in combined_meaning.lower():
        combined_meaning = re.sub(r"\s*\(idiom\)\s*", "", combined_meaning, flags=re.IGNORECASE)
        combined_meaning = "<b>idiom</b> " + combined_meaning.strip()

    # Handle subject/domain markers
    domain_markers = {
        r"\(fig\.\)": "figurative",
        r"\bphysics\b": "physics",
        r"\bphilosophy\b": "philosophy",
        r"\bLIT\b": "literary",
    }

    for pattern, display_text in domain_markers.items():
        replacement = f'<span color="red">{display_text}</span>'
        combined_meaning = re.sub(pattern, replacement, combined_meaning, flags=re.IGNORECASE)

    # Handle full parts of speech - skip if already inside HTML tags
    for pos in parts_of_speech:
        pattern = rf"(?<!<b>)\b{pos}\b(?!</b>)"
        combined_meaning = re.sub(pattern, f"<b>{pos}</b>", combined_meaning, flags=re.IGNORECASE)

    return combined_meaning, examples if examples else None


def extract_examples_from_text(text: str) -> Tuple[str, Optional[List[str]]]:
    """Extract examples from a text section, returning cleaned meaning and examples."""

    # Handle abbreviation pattern: "abbreviation = [number][chinese][pinyin][chinese] english_translation"
    # Note: Pleco exports may contain private use area Unicode characters, so we need a more flexible pattern
    abbrev_match = re.search(
        r"abbreviation\s*=\s*[\uE000-\uF8FF\d]*[一-龯]+[\uE000-\uF8FF\da-z]*[一-龯]+[\uE000-\uF8FF]*\s+(.+)$", text
    )
    if abbrev_match:
        # Extract just the English translation at the end, but preserve any part of speech at the beginning
        english_part = abbrev_match.group(1).strip()

        # Check if the text starts with a part of speech
        pos_match = re.match(
            r"^(verb|noun|adjective|adverb|pronoun|preposition|conjunction|interjection|idiom)\s+", text, re.IGNORECASE
        )
        if pos_match:
            pos_word = pos_match.group(1)
            meaning = f"{pos_word} {english_part}"
        else:
            meaning = english_part

        return meaning, None

    # Find the first occurrence of Chinese characters - this marks start of examples
    chinese_match = re.search(r"[一-龯]", text)

    if chinese_match:
        # Everything before Chinese characters is the core meaning
        meaning = text[: chinese_match.start()].strip()
        # Everything from Chinese characters onwards are examples
        examples_text = text[chinese_match.start() :].strip()
        examples = [examples_text] if examples_text else None
    else:
        # No Chinese characters, just the meaning
        meaning = text.strip()
        examples = None

    # Clean up extra spaces
    meaning = re.sub(r"\s+", " ", meaning).strip()

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
