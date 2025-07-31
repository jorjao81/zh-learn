"""
Step definitions for character decomposition BDD scenarios.
"""

from behave import given, when, then
from anki_pleco_importer.character_decomposer import CharacterDecomposer, ComponentType
from anki_pleco_importer.chinese import get_structural_decomposition


@given("the CharacterDecomposer is available")
def step_character_decomposer_available(context):
    """Initialize the CharacterDecomposer."""
    context.decomposer = CharacterDecomposer()


@given('I have a Chinese character "{character}"')
def step_given_character(context, character):
    """Store the character to decompose."""
    context.character = character


@given('I have an invalid input "{input_text}"')
def step_given_invalid_input(context, input_text):
    """Store invalid input."""
    context.character = input_text


@given('I have an empty input ""')
def step_given_empty_input(context):
    """Store empty input."""
    context.character = ""


@when("I decompose it")
def step_when_decompose(context):
    """Decompose the character."""
    context.result = context.decomposer.decompose(context.character)


@when("I try to decompose it")
def step_when_try_decompose(context):
    """Try to decompose with error handling."""
    try:
        context.result = context.decomposer.decompose(context.character)
        context.error = None
    except Exception as e:
        context.error = str(e)
        context.result = None


@then("I should get the following components")
def step_then_check_components(context):
    """Check that decomposition results match expected components."""
    expected_components = []
    expected_meanings = []
    expected_types = []
    expected_pinyin = []

    for row in context.table:
        expected_components.append(row["component"])
        expected_meanings.append(row["meaning"])

        # Handle pinyin column if present
        if "pinyin" in row.headings:
            pinyin_val = row["pinyin"].strip()
            expected_pinyin.append(pinyin_val if pinyin_val else None)

        # Convert string to ComponentType enum
        type_str = row["type"]
        if type_str == "semantic":
            expected_types.append(ComponentType.SEMANTIC)
        elif type_str == "phonetic":
            expected_types.append(ComponentType.PHONETIC)
        elif type_str == "pictographic":
            expected_types.append(ComponentType.PICTOGRAPHIC)
        else:
            expected_types.append(ComponentType.UNKNOWN)

    assert context.result is not None, "Decomposition result should not be None"
    assert (
        context.result.components == expected_components
    ), f"Expected components {expected_components}, got {context.result.components}"
    assert (
        context.result.radical_meanings == expected_meanings
    ), f"Expected meanings {expected_meanings}, got {context.result.radical_meanings}"
    assert (
        context.result.component_types == expected_types
    ), f"Expected types {expected_types}, got {context.result.component_types}"

    # Check pinyin if provided
    if expected_pinyin:
        assert (
            context.result.component_pinyin == expected_pinyin
        ), f"Expected pinyin {expected_pinyin}, got {context.result.component_pinyin}"


@then('the structure notes should be "{expected_notes}"')
def step_then_check_structure_notes(context, expected_notes):
    """Check that structure notes match expected value."""
    assert context.result is not None, "Decomposition result should not be None"
    assert context.result.structure_notes == expected_notes, (
        f"Expected structure notes '{expected_notes}', " f"got '{context.result.structure_notes}'"
    )


@then('I should get an error "{expected_error}"')
def step_then_check_error(context, expected_error):
    """Check that the expected error was raised."""
    assert context.error is not None, "Expected an error but none was raised"
    assert context.error == expected_error, f"Expected error '{expected_error}', got '{context.error}'"


@given("I have the following Anki export dictionary")
def step_given_anki_dictionary(context):
    """Store the Anki export dictionary."""
    context.anki_dictionary = {}
    for row in context.table:
        chinese = row["chinese"]
        pinyin = row["pinyin"]
        definition = row["definition"]
        context.anki_dictionary[chinese] = {"pinyin": pinyin, "definition": definition}


@given("I have the following Anki export dictionary with mixed note types")
def step_given_anki_dictionary_mixed_note_types(context):
    """Store the Anki export dictionary with note types."""
    from anki_pleco_importer.anki_parser import AnkiCard, AnkiExportParser

    # Create mock AnkiCard objects with different note types
    cards = []
    for row in context.table:
        chinese = row["chinese"]
        pinyin = row["pinyin"]
        definition = row["definition"]
        notetype = row["notetype"]

        card = AnkiCard(notetype=notetype, pinyin=pinyin, characters=chinese, audio="", definitions=definition)
        cards.append(card)

    # Create mock AnkiExportParser
    context.anki_parser = AnkiExportParser()
    context.anki_parser.cards = cards


@when('I decompose the 3-character word "{word}"')
def step_when_decompose_3_char_word(context, word):
    """Decompose a 3-character word using dictionary lookup."""
    context.word = word
    context.result_decomposition = get_structural_decomposition(word, context.anki_dictionary)


@when('I decompose the 4-character word "{word}"')
def step_when_decompose_4_char_word(context, word):
    """Decompose a 4-character word using dictionary lookup."""
    context.word = word
    context.result_decomposition = get_structural_decomposition(word, context.anki_dictionary)


@when('I decompose the 5-character word "{word}"')
def step_when_decompose_5_char_word(context, word):
    """Decompose a 5-character word using dictionary lookup."""
    context.word = word
    context.result_decomposition = get_structural_decomposition(word, context.anki_dictionary)


@when('I decompose the 4-character word "{word}" using the Anki parser')
def step_when_decompose_4_char_word_with_parser(context, word):
    """Decompose a 4-character word using AnkiExportParser."""
    from anki_pleco_importer.pleco import _create_anki_dictionary
    from anki_pleco_importer.chinese import get_structural_decomposition

    context.word = word
    # Use the actual function that needs to be fixed
    anki_dictionary = _create_anki_dictionary(context.anki_parser)
    context.result_decomposition = get_structural_decomposition(word, anki_dictionary)


@then('I should get the structural decomposition "{expected_decomposition}"')
def step_then_check_structural_decomposition(context, expected_decomposition):
    """Check that the structural decomposition matches expected value."""
    assert context.result_decomposition == expected_decomposition, (
        f"Expected decomposition '{expected_decomposition}', " f"got '{context.result_decomposition}'"
    )
