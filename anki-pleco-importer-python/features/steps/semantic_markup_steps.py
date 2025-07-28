"""Step definitions for semantic markup feature."""

from behave import given, when, then
from anki_pleco_importer.pleco import (
    parse_pleco_definition_semantic,
    format_examples_with_semantic_markup,
)
from anki_pleco_importer.character_decomposer import (
    CharacterDecomposer,
    ComponentResult,
    ComponentType,
)
from anki_pleco_importer.chinese import format_components_semantic


@given("the semantic markup conversion function is available")
def step_semantic_markup_available(context):
    """Semantic markup conversion functions are available."""
    context.semantic_markup_available = True


@when("I convert them to Anki cards with semantic markup")
def step_convert_to_semantic_markup(context):
    """Convert Pleco entries to semantic markup."""
    context.semantic_results = []

    # Use the pleco_entries that were created by the previous step
    for entry in context.pleco_entries:
        # Parse definition with semantic markup
        formatted_meaning, examples, similar_chars = parse_pleco_definition_semantic(entry.definition)

        # Convert pinyin (this would normally be done by the conversion process)
        from anki_pleco_importer.chinese import convert_numbered_pinyin_to_tones

        tone_pinyin = convert_numbered_pinyin_to_tones(entry.pinyin)

        context.semantic_results.append(
            {
                "simplified": entry.chinese,
                "pinyin": tone_pinyin,
                "meaning": formatted_meaning,
                "examples": format_examples_with_semantic_markup(examples) if examples else None,
            }
        )


@then("I should get the following semantic HTML")
def step_verify_semantic_html(context):
    """Verify the semantic HTML output matches expected."""
    for i, row in enumerate(context.table):
        # Handle different test scenarios with different column structures

        # Character decomposition tests
        if "character" in row and "expected_decomposition" in row:
            expected_character = row["character"]
            expected_decomposition = row["expected_decomposition"]

            actual = context.decomposition_results[i]

            assert (
                actual["character"] == expected_character
            ), f"Character mismatch: got {actual['character']}, expected {expected_character}"
            assert (
                actual["decomposition"] == expected_decomposition
            ), f"Decomposition mismatch: got {actual['decomposition']}, expected {expected_decomposition}"

        # Word decomposition tests
        elif "word" in row and "expected_decomposition" in row:
            expected_word = row["word"]
            expected_decomposition = row["expected_decomposition"]

            actual = context.word_decomposition_results[i]

            assert actual["word"] == expected_word, f"Word mismatch: got {actual['word']}, expected {expected_word}"
            assert (
                actual["decomposition"] == expected_decomposition
            ), f"Decomposition mismatch: got {actual['decomposition']}, expected {expected_decomposition}"

        # Examples tests
        elif "expected_examples" in row:
            expected_simplified = row["chinese"]  # Use "chinese" column instead of "simplified"
            expected_pinyin = row["expected_pinyin"]
            expected_examples = row["expected_examples"]

            actual = context.semantic_results[i]

            assert (
                actual["simplified"] == expected_simplified
            ), f"Simplified mismatch: got {actual['simplified']}, expected {expected_simplified}"
            assert (
                actual["pinyin"] == expected_pinyin
            ), f"Pinyin mismatch: got {actual['pinyin']}, expected {expected_pinyin}"
            assert (
                actual["examples"] == expected_examples
            ), f"Examples mismatch: got {actual['examples']}, expected {expected_examples}"

        # Standard meaning tests
        else:
            expected_simplified = row["simplified"]
            expected_pinyin = row["pinyin"]
            expected_meaning = row["meaning"]

            actual = context.semantic_results[i]

            assert (
                actual["simplified"] == expected_simplified
            ), f"Simplified mismatch: got {actual['simplified']}, expected {expected_simplified}"
            assert (
                actual["pinyin"] == expected_pinyin
            ), f"Pinyin mismatch: got {actual['pinyin']}, expected {expected_pinyin}"
            assert (
                actual["meaning"] == expected_meaning
            ), f"Meaning mismatch: got {actual['meaning']}, expected {expected_meaning}"

            # Check examples if present in expected results
            if "examples" in row:
                expected_examples = row["examples"]
                assert (
                    actual["examples"] == expected_examples
                ), f"Examples mismatch: got {actual['examples']}, expected {expected_examples}"


@given("I have the following character decomposition")
def step_given_character_decomposition(context):
    """Set up character decomposition data."""
    context.character_decompositions = []

    for row in context.table:
        # Parse the components, meanings, types, and pinyin from the BDD table
        import json

        components = json.loads(row["components"])
        radical_meanings = json.loads(row["radical_meanings"])
        component_types_str = json.loads(row["component_types"])
        component_pinyin = json.loads(row["component_pinyin"])

        # Convert string types to ComponentType enums
        component_types = []
        for type_str in component_types_str:
            if type_str == "semantic":
                component_types.append(ComponentType.SEMANTIC)
            elif type_str == "phonetic":
                component_types.append(ComponentType.PHONETIC)
            else:
                component_types.append(ComponentType.UNKNOWN)

        component_result = ComponentResult(
            character=row["character"],
            components=components,
            radical_meanings=radical_meanings,
            component_types=component_types,
            component_pinyin=component_pinyin,
            structure_notes=row["structure_notes"],
        )

        context.character_decompositions.append(component_result)


@when("I convert the decomposition to semantic markup")
def step_convert_decomposition_semantic(context):
    """Convert character decomposition to semantic markup."""
    context.decomposition_results = []

    decomposer = CharacterDecomposer()

    for decomposition in context.character_decompositions:
        semantic_html = decomposer.format_decomposition_semantic(decomposition)
        context.decomposition_results.append({"character": decomposition.character, "decomposition": semantic_html})


@given("I have the following word decomposition")
def step_given_word_decomposition(context):
    """Set up word decomposition data."""
    context.word_decompositions = []

    for row in context.table:
        import json

        components = json.loads(row["components"])
        component_pinyin = json.loads(row["component_pinyin"])
        component_definitions = json.loads(row["component_definitions"])

        # Convert to the format expected by format_components_semantic
        components_data = []
        for i, component in enumerate(components):
            components_data.append(
                {"chinese": component, "pinyin": component_pinyin[i], "definition": component_definitions[i]}
            )

        context.word_decompositions.append({"word": row["word"], "components": components_data})


@when("I convert the word decomposition to semantic markup")
def step_convert_word_decomposition_semantic(context):
    """Convert word decomposition to semantic markup."""
    context.word_decomposition_results = []

    for decomposition in context.word_decompositions:
        semantic_html = format_components_semantic(decomposition["components"])
        context.word_decomposition_results.append({"word": decomposition["word"], "decomposition": semantic_html})
