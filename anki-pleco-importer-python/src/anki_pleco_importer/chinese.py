"""Chinese language processing utilities."""

from typing import Match
import re
import logging
from hanzipy.dictionary import HanziDictionary  # type: ignore

# Suppress debug output from hanzipy library
logging.getLogger("root").setLevel(logging.WARNING)

# Initialize HanziDictionary at module level for performance
_hanzi_dictionary = HanziDictionary()


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


def get_semantic_components(chinese_text: str) -> str:
    """Get semantic components for Chinese characters using hanzipy.

    Args:
        chinese_text: Chinese text to decompose

    Returns:
        Formatted string with characters and their meanings joined by +
        Format: 字(pinyin - meaning) + 字(pinyin - meaning)
    """
    components = []

    # Split text into individual characters
    for char in chinese_text:
        # Skip non-Chinese characters
        if not "\u4e00" <= char <= "\u9fff":
            continue

        try:
            # Get pinyin (prefer lowercase/common pronunciation)
            pinyin_list = _hanzi_dictionary.get_pinyin(char)
            if not pinyin_list:
                continue

            # Prefer lowercase pinyin over uppercase (common vs proper name)
            pinyin = pinyin_list[0]
            for p in pinyin_list:
                if p.islower():
                    pinyin = p
                    break

            # Get all definitions
            definitions = _hanzi_dictionary.definition_lookup(char)
            if not definitions:
                continue

            # Collect all definitions, excluding surname definitions
            all_definitions = []
            for def_item in definitions:
                definition_text = def_item.get("definition", "")
                if "surname" not in definition_text.lower() and definition_text:
                    all_definitions.append(definition_text)

            # If no non-surname definitions found, use the first one
            if not all_definitions:
                all_definitions = [definitions[0].get("definition", "")]

            # Join all definitions with forward slash separator
            combined_definition = "/".join(all_definitions)

            # Convert numbered pinyin to toned pinyin for display
            pinyin_clean = convert_numbered_pinyin_to_tones(pinyin)

            # Format as: 字(pinyin - meaning)
            component = f"{char}({pinyin_clean} - {combined_definition})"
            components.append(component)

        except Exception:
            # If any error occurs, skip this character
            continue

    # Join with + sign
    return " + ".join(components)
