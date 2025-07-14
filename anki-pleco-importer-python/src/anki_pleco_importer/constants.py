"""Constants and configuration for Pleco to Anki conversion."""

import re

# Constants definitions

# Parts of speech that should be formatted with bold tags
PARTS_OF_SPEECH = [
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

# Abbreviations for parts of speech
PART_OF_SPEECH_ABBREVIATIONS = {
    r"\bV\.\s*": "<b>verb</b> ",
    r"\bN\.\s*": "<b>noun</b> ",
    r"\bAdj\.\s*": "<b>adjective</b> ",
    r"\bAdv\.\s*": "<b>adverb</b> ",
}

# Domain markers that should be highlighted in red
DOMAIN_MARKERS = {
    r"\(fig\.\)": "figurative",
    r"\bphysics\b": "physics",
    r"\bphilosophy\b": "philosophy",
    r"\bLIT\b": "literary",
    r"\bdialect\b": "dialect",
    r"\bbiology\b": "biology",
    r"\bstatistics\b": "statistics",
    r"\bmathematics\b": "mathematics",
    r"\bliterary\b": "literary",
}

# Regex patterns for Chinese example extraction
CHINESE_EXAMPLE_PATTERNS = {
    # Pattern 1: Chinese sentence with punctuation + pinyin + English with punctuation
    "sentence_with_punctuation": r"[一-龯][^.。]*[.。]\s+[A-Za-z][^.]*?[.!?]\s*(?:[A-Z][^.]*?[.!?]\s*)*",
    # Pattern 2: Chinese phrase at the end + space + pinyin + space + English
    "remaining_chinese": r"[一-龯][^$]*$",
}

# Abbreviation pattern for definitions like "abbreviation = [stuff] translation"
ABBREVIATION_PATTERN = (
    r"abbreviation\s*=\s*[\uE000-\uF8FF\d]*[一-龯]+[\uE000-\uF8FF\da-z]*[一-龯]+[\uE000-\uF8FF]*\s+(.+)$"
)

# Pre-compiled regex patterns for performance
COMPILED_PATTERNS = {
    "chinese_chars": re.compile(r"[一-龯]"),
    "abbreviation": re.compile(ABBREVIATION_PATTERN),
    "idiom_parentheses": re.compile(r"\s*\(idiom\)\s*", re.IGNORECASE),
    "whitespace_cleanup": re.compile(r"\s+"),
}

# Pre-compile domain marker patterns
COMPILED_DOMAIN_PATTERNS = {
    re.compile(pattern, re.IGNORECASE): display_text for pattern, display_text in DOMAIN_MARKERS.items()
}

# Pre-compile parts of speech patterns
COMPILED_POS_PATTERNS = {pos: re.compile(rf"(?<!<b>)\b{pos}\b(?!</b>)", re.IGNORECASE) for pos in PARTS_OF_SPEECH}

# Pre-compile abbreviation patterns
COMPILED_ABBREV_PATTERNS = {
    re.compile(pattern, re.IGNORECASE): replacement for pattern, replacement in PART_OF_SPEECH_ABBREVIATIONS.items()
}
