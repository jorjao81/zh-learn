from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterator, Match
import re
from pydantic import BaseModel


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


class AnkiCard(BaseModel):
    """Represents an Anki flashcard with Chinese learning fields."""

    pinyin: str
    simplified: str
    pronunciation: Optional[str] = None
    meaning: str
    examples: Optional[List[str]] = None
    phonetic_component: Optional[str] = None
    semantic_component: Optional[str] = None
    similar_characters: Optional[List[str]] = None
    passive: bool = False
    alternate_pronunciations: Optional[List[str]] = None
    nohearing: bool = False


def convert_numbered_pinyin_to_tones(pinyin: str) -> str:
    """Convert numbered pinyin (e.g., 'ni3hao3') to pinyin with tone marks (e.g., 'nǐhǎo')."""
    # Tone mark mappings for each vowel
    tone_marks = {
        "a": ["a", "ā", "á", "ǎ", "à"],
        "e": ["e", "ē", "é", "ě", "è"],
        "i": ["i", "ī", "í", "ǐ", "ì"],
        "o": ["o", "ō", "ó", "ǒ", "ò"],
        "u": ["u", "ū", "ú", "ǔ", "ù"],
        "ü": ["ü", "ǖ", "ǘ", "ǚ", "ǜ"],
        "v": ["v", "ǖ", "ǘ", "ǚ", "ǜ"],  # v is sometimes used for ü
        "A": ["A", "Ā", "Á", "Ǎ", "À"],
        "E": ["E", "Ē", "É", "Ě", "È"],
        "I": ["I", "Ī", "Í", "Ǐ", "Ì"],
        "O": ["O", "Ō", "Ó", "Ǒ", "Ò"],
        "U": ["U", "Ū", "Ú", "Ǔ", "Ù"],
        "Ü": ["Ü", "Ǖ", "Ǘ", "Ǚ", "Ǜ"],
        "V": ["V", "Ǖ", "Ǘ", "Ǚ", "Ǜ"],  # V is sometimes used for Ü
    }

    def replace_syllable(match: Match[str]) -> str:
        syllable = match.group(1)
        tone = int(match.group(2))

        if tone == 5 or tone == 0:  # Neutral tone
            return syllable

        if tone > 5 or tone < 1:  # Invalid tone, return as-is
            return match.group(0)

        # Find the vowel to apply the tone mark to (case insensitive)
        # Priority: a > e > ou > o > i/u (whichever comes last)
        syllable_lower = syllable.lower()

        if "a" in syllable_lower:
            vowel = "a"
            pos = syllable_lower.index("a")
        elif "e" in syllable_lower:
            vowel = "e"
            pos = syllable_lower.index("e")
        elif "ou" in syllable_lower:
            vowel = "o"
            pos = syllable_lower.index("o")
        elif "o" in syllable_lower:
            vowel = "o"
            pos = syllable_lower.index("o")
        elif "i" in syllable_lower and "u" in syllable_lower:
            # Choose the one that comes last
            i_pos = syllable_lower.rindex("i")
            u_pos = syllable_lower.rindex("u")
            if i_pos > u_pos:
                vowel = "i"
                pos = i_pos
            else:
                vowel = "u"
                pos = u_pos
        elif "i" in syllable_lower:
            vowel = "i"
            pos = syllable_lower.rindex("i")
        elif "u" in syllable_lower:
            vowel = "u"
            pos = syllable_lower.rindex("u")
        elif "ü" in syllable_lower or "v" in syllable_lower:
            vowel = "ü" if "ü" in syllable_lower else "v"
            pos = syllable_lower.index(vowel)
        else:
            return syllable  # No vowel found, return as is

        # Get the original vowel to preserve case
        original_vowel = syllable[pos]

        # Use the original vowel (with case) as the key for tone marks
        tone_key = original_vowel if original_vowel in tone_marks else vowel

        # Replace the vowel with the toned version
        if tone_key in tone_marks and tone < len(tone_marks[tone_key]):
            toned_vowel = tone_marks[tone_key][tone]
            return syllable[:pos] + toned_vowel + syllable[pos + 1 :]

        return syllable

    # Pattern to match syllables with tone numbers (including 0)
    pattern = r"([a-züvA-ZÜVA-Z]+?)([0-5])"
    result = re.sub(pattern, replace_syllable, pinyin)

    return result


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
    # Extract just the definition part before the first Chinese example
    # Look for where Chinese characters start (these are examples)

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

    return AnkiCard(
        pinyin=convert_numbered_pinyin_to_tones(pleco_entry.pinyin),
        simplified=pleco_entry.chinese,
        meaning=meaning,
        examples=examples,
    )
