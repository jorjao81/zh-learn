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


def get_structural_decomposition(chinese_text: str, anki_dictionary: dict) -> str:
    """Get structural decomposition for Chinese characters using CharacterDecomposer.

    Args:
        chinese_text: Chinese text to decompose
        anki_dictionary: Optional dictionary from Anki export for word decomposition

    Returns:
        Formatted string with structural decomposition
        Format: 字(pinyin - meaning) + 字(pinyin - meaning)
    """
    # For multi-character words (3+ characters), use dictionary-based decomposition
    if len(chinese_text) > 2:
        return _get_dictionary_based_decomposition(chinese_text, anki_dictionary)

    # For 2-character words, fall back to individual character definitions
    elif len(chinese_text) == 2:
        return _get_individual_character_definitions(chinese_text)

    # For single characters, use proper structural decomposition
    try:
        from .character_decomposer import CharacterDecomposer

        decomposer = CharacterDecomposer()
        result = decomposer.decompose(chinese_text)
        return result.structure_notes
    except (ImportError, Exception):
        # Fall back to individual character definitions if decomposer fails
        return _get_individual_character_definitions(chinese_text)


def get_structural_decomposition_semantic(chinese_text: str, anki_dictionary: dict) -> str:
    """Get structural decomposition for Chinese characters using semantic markup.

    Args:
        chinese_text: Chinese text to decompose
        anki_dictionary: Optional dictionary from Anki export for word decomposition

    Returns:
        Formatted string with structural decomposition using semantic HTML markup
    """
    # For multi-character words (3+ characters), use dictionary-based decomposition
    if len(chinese_text) > 2:
        return _get_dictionary_based_decomposition_semantic(chinese_text, anki_dictionary)

    # For 2-character words, fall back to individual character definitions with semantic markup
    elif len(chinese_text) == 2:
        return _get_individual_character_definitions_semantic(chinese_text)

    # For single characters, use proper structural decomposition with semantic markup
    try:
        from .character_decomposer import CharacterDecomposer

        decomposer = CharacterDecomposer()
        result = decomposer.decompose(chinese_text)
        return decomposer.format_decomposition_semantic(result)
    except (ImportError, Exception):
        # Fall back to individual character definitions if decomposer fails
        return _get_individual_character_definitions_semantic(chinese_text)


def _get_dictionary_based_decomposition(chinese_text: str, anki_dictionary: dict) -> str:
    """Decompose multi-character words using Anki dictionary lookup.

    Args:
        chinese_text: Chinese text to decompose (3+ characters)
        anki_dictionary: Dictionary mapping Chinese words to their pinyin and
            definitions

    Returns:
        Formatted string with word decomposition
        Format: 词(pinyin - meaning) + 词(pinyin - meaning)
    """

    # For 4-character words, prefer 2+2 split
    if len(chinese_text) == 4:
        components = _find_optimal_4_char_decomposition(chinese_text, anki_dictionary)
        if components:
            return _format_components(components)

    # For other lengths, use greedy longest-match decomposition
    components = _find_greedy_decomposition(chinese_text, anki_dictionary)
    if components:
        return _format_components(components)

    # Fall back to individual character definitions if no matches found
    return _get_individual_character_definitions(chinese_text)


def _get_dictionary_based_decomposition_semantic(chinese_text: str, anki_dictionary: dict) -> str:
    """Decompose multi-character words using Anki dictionary lookup with semantic markup.

    Args:
        chinese_text: Chinese text to decompose (3+ characters)
        anki_dictionary: Dictionary mapping Chinese words to their pinyin and
            definitions

    Returns:
        Formatted string with word decomposition using semantic HTML markup
    """

    # For 4-character words, prefer 2+2 split
    if len(chinese_text) == 4:
        components = _find_optimal_4_char_decomposition(chinese_text, anki_dictionary)
        if components:
            return format_components_semantic(components)

    # For other lengths, use greedy longest-match decomposition
    components = _find_greedy_decomposition(chinese_text, anki_dictionary)
    if components:
        return format_components_semantic(components)

    # Fall back to individual character definitions if no matches found
    return _get_individual_character_definitions_semantic(chinese_text)


def _find_optimal_4_char_decomposition(chinese_text: str, anki_dictionary: dict) -> list:
    """Find optimal decomposition for 4-character word preferring 2+2 split."""
    # Try 2+2 split first
    left_part = chinese_text[:2]
    right_part = chinese_text[2:]

    if left_part in anki_dictionary and right_part in anki_dictionary:
        return [
            _create_component(left_part, anki_dictionary[left_part]),
            _create_component(right_part, anki_dictionary[right_part]),
        ]

    # Fall back to greedy decomposition
    return _find_greedy_decomposition(chinese_text, anki_dictionary)


def _find_greedy_decomposition(chinese_text: str, anki_dictionary: dict) -> list:
    """Find decomposition using greedy longest-match algorithm."""
    components = []
    i = 0

    while i < len(chinese_text):
        # Try to find the longest match starting from position i
        best_match = None
        best_length = 0

        # Special rule: For multi-character words, don't allow matching the entire word as single component
        max_length = len(chinese_text) - i
        if len(chinese_text) > 1 and i == 0:  # If this is start of multi-char word
            max_length = min(max_length, len(chinese_text) - 1)  # Don't match the entire word

        for length in range(min(max_length, 4), 0, -1):  # Try lengths 4, 3, 2, 1
            candidate = chinese_text[i : i + length]
            if candidate in anki_dictionary:
                best_match = candidate
                best_length = length
                break

        if best_match:
            components.append(_create_component(best_match, anki_dictionary[best_match]))
            i += best_length
        else:
            # No match found, use individual character
            char = chinese_text[i]
            components.append(_create_individual_character_component(char))
            i += 1

    return components


def _create_component(chinese_word: str, word_info: dict) -> dict:
    """Create a component from dictionary entry."""
    pinyin = word_info.get("pinyin", "")
    definition = word_info.get("definition", "")

    # Convert numbered pinyin to toned pinyin
    pinyin_clean = convert_numbered_pinyin_to_tones(pinyin)

    return {"chinese": chinese_word, "pinyin": pinyin_clean, "definition": definition}


def _create_individual_character_component(char: str) -> dict:
    """Create a component for individual character using HanziDictionary."""
    try:
        # Get pinyin (prefer lowercase/common pronunciation)
        pinyin_list = _hanzi_dictionary.get_pinyin(char)
        if not pinyin_list:
            return {"chinese": char, "pinyin": "", "definition": ""}

        # Prefer lowercase pinyin over uppercase (common vs proper name)
        pinyin = pinyin_list[0]
        for p in pinyin_list:
            if p.islower():
                pinyin = p
                break

        # Get all definitions
        definitions = _hanzi_dictionary.definition_lookup(char)
        if not definitions:
            return {"chinese": char, "pinyin": "", "definition": ""}

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

        # Clean unwanted patterns from the definition
        cleaned_definition = clean_character_definition(combined_definition)

        # Convert numbered pinyin to toned pinyin for display
        pinyin_clean = convert_numbered_pinyin_to_tones(pinyin)

        return {
            "chinese": char,
            "pinyin": pinyin_clean,
            "definition": cleaned_definition,
        }
    except Exception:
        return {"chinese": char, "pinyin": "", "definition": ""}


def _format_components(components: list) -> str:
    """Format components into the final decomposition string."""
    if not components:
        return ""

    # Check for single multi-character component which violates our rule
    if len(components) == 1 and len(components[0]["chinese"]) > 1:
        # Force decomposition into individual characters
        chinese_word = components[0]["chinese"]
        char_components = []
        for char in chinese_word:
            char_component = _create_individual_character_component(char)
            char_components.append(char_component)
        return _format_components(char_components)

    formatted_parts = []

    for component in components:
        chinese = component["chinese"]
        pinyin = component["pinyin"]
        definition = component["definition"]

        # Format as: 字 pinyin meaning
        formatted_part = f"{chinese} {pinyin} {definition}"
        formatted_parts.append(formatted_part)

    return " + ".join(formatted_parts)


def format_components_semantic(components: list) -> str:
    """Format word components with semantic HTML markup."""
    if not components:
        return ""

    if len(components) == 1:
        # Single component - check if it's a multi-character word that shouldn't be single
        component = components[0]
        chinese = component["chinese"]

        # For multi-character components, this violates our rule - decompose by character
        if len(chinese) > 1:
            # Force decomposition into individual characters
            char_components = []
            for char in chinese:
                char_component = _create_individual_character_component(char)
                char_components.append(char_component)
            return format_components_semantic(char_components)

        # Single character component is OK
        pinyin = component["pinyin"]
        definition = component["definition"]

        result = f'<span class="hanzi">{chinese}</span>'
        if pinyin:
            result += f' <span class="pinyin">{pinyin}</span>'
        if definition:
            result += f' <span class="definition">{definition}</span>'
        return result

    # Multiple components - create semantic HTML list
    component_items = []
    for component in components:
        chinese = component["chinese"]
        pinyin = component["pinyin"]
        definition = component["definition"]

        component_html = f'<span class="hanzi">{chinese}</span>'
        if pinyin:
            component_html += f' <span class="pinyin">{pinyin}</span>'
        if definition:
            component_html += f' <span class="definition">{definition}</span>'

        component_items.append(component_html)

    list_items = "</li><li>".join(component_items)
    return f"<ul><li>{list_items}</li></ul>"


def _get_individual_character_definitions(chinese_text: str) -> str:
    """Get individual character definitions as fallback for structural decomposition.

    Args:
        chinese_text: Chinese text to get definitions for

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

            # Clean unwanted patterns from the definition
            cleaned_definition = clean_character_definition(combined_definition)

            # Convert numbered pinyin to toned pinyin for display
            pinyin_clean = convert_numbered_pinyin_to_tones(pinyin)

            # Format as: 字 pinyin meaning
            component = f"{char} {pinyin_clean} {cleaned_definition}"
            components.append(component)

        except Exception:
            # If any error occurs, skip this character
            continue

    # Join with + sign
    return " + ".join(components)


def _get_individual_character_definitions_semantic(chinese_text: str) -> str:
    """Get individual character definitions with semantic markup as fallback for structural decomposition.

    Args:
        chinese_text: Chinese text to get definitions for

    Returns:
        Formatted string with characters and their meanings using semantic HTML markup
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

            # Clean unwanted patterns from the definition
            cleaned_definition = clean_character_definition(combined_definition)

            # Convert numbered pinyin to toned pinyin for display
            pinyin_clean = convert_numbered_pinyin_to_tones(pinyin)

            # Format with semantic markup: 字 (pinyin) - definition
            component_dict = {"chinese": char, "pinyin": pinyin_clean, "definition": cleaned_definition}
            components.append(component_dict)

        except Exception:
            # If any error occurs, skip this character
            continue

    # Use semantic formatting
    return format_components_semantic(components)


def clean_character_definition(definition: str) -> str:
    """Clean unwanted patterns from single character definitions.

    Removes patterns like:
    - CL:場|场[chang3] (classifier patterns)
    - variant of X[pinyin] (variant patterns)
    - old variant of X[pinyin] (old variant patterns)

    Args:
        definition: Raw character definition string

    Returns:
        Cleaned definition string with unwanted patterns removed
    """
    if not definition:
        return definition

    import re

    # Pattern 1: Remove CL:X|Y[pinyin] patterns (classifier patterns)
    # Matches: CL:場|场[chang3], CL:個|个[ge4], CL:座[zuo4], etc.
    cl_pattern = r"/CL:[^/]+"
    definition = re.sub(cl_pattern, "", definition)

    # Pattern 2: Remove "variant of X[pinyin]" patterns
    # Matches: variant of 屌[diao3], variant of 莊|庄[zhuang1], variant of 歲|岁[sui4], etc.
    variant_pattern = r"/variant of [一-龯]+(?:\|[一-龯]+)?\[[^\]]+\]"
    definition = re.sub(variant_pattern, "", definition)

    # Pattern 3: Remove "old variant of X[pinyin]" patterns
    # Matches: old variant of 鼓[gu3], old variant of 莊|庄[zhuang1], etc.
    old_variant_pattern = r"/old variant of [一-龯]+(?:\|[一-龯]+)?\[[^\]]+\]"
    definition = re.sub(old_variant_pattern, "", definition)

    # Pattern 4: Remove standalone "variant of X[pinyin]" at the beginning (with or without trailing slash)
    # Matches: "variant of 棋[qi2]/" or "variant of 莊|庄[zhuang1]" at start of definition
    start_variant_pattern = r"^variant of [一-龯]+(?:\|[一-龯]+)?\[[^\]]+\]/?"
    definition = re.sub(start_variant_pattern, "", definition)

    # Pattern 5: Remove standalone "old variant of X[pinyin]" at the beginning (with or without trailing slash)
    # Matches: "old variant of 鼓[gu3]/" or "old variant of 莊|庄[zhuang1]" at start of definition
    start_old_variant_pattern = r"^old variant of [一-龯]+(?:\|[一-龯]+)?\[[^\]]+\]/?"
    definition = re.sub(start_old_variant_pattern, "", definition)

    # Clean up any leftover separators and whitespace
    # Remove leading/trailing slashes
    definition = definition.strip("/")

    # Remove double slashes created by removals
    definition = re.sub(r"/+", "/", definition)

    # Remove leading/trailing whitespace
    definition = definition.strip()

    return definition
