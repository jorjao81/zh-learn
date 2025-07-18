"""Step definitions for Pleco to Anki conversion BDD tests."""

from behave import given, when, then
from anki_pleco_importer.pleco import PlecoEntry, pleco_to_anki
from anki_pleco_importer.anki_parser import AnkiExportParser, AnkiCard


# Core conversion step definitions


@given("the pleco_to_anki conversion function is available")
def step_conversion_function_available(context):
    """Verify the pleco_to_anki conversion function is available."""
    context.conversion_available = True


@given("I have the following Pleco entries")
@given("I have the following Pleco entry")
def step_have_pleco_entries(context):
    """Create Pleco entries from table data (handles both single and multiple)."""
    context.pleco_entries = []
    for row in context.table:
        entry = PlecoEntry(chinese=row["chinese"], pinyin=row["pinyin"], definition=row["definition"])
        context.pleco_entries.append(entry)

    # For backward compatibility with single entry scenarios
    if len(context.pleco_entries) == 1:
        context.pleco_entry = context.pleco_entries[0]


@given('I have a Pleco entry with chinese "{chinese}", pinyin "{pinyin}", and definition "{definition}"')
def step_have_pleco_entry_with_values(context, chinese, pinyin, definition):
    """Create a Pleco entry with specific values."""
    context.pleco_entry = PlecoEntry(chinese=chinese, pinyin=pinyin, definition=definition)


@given('I have a Pleco entry with definition "{definition}"')
def step_have_pleco_entry_with_definition(context, definition):
    """Create a Pleco entry with just a definition (for example parsing tests)."""
    context.pleco_entry = PlecoEntry(chinese="测试", pinyin="cèshì", definition=definition)  # Test word  # Test pinyin


@when("I convert them to Anki cards")
@when("I convert it to an Anki card")
def step_convert_to_anki(context):
    """Convert Pleco entries to Anki cards (handles both single and multiple)."""
    # Create a mock AnkiExportParser for tests
    anki_export_parser = AnkiExportParser()

    if hasattr(context, "pleco_entries"):
        # Convert multiple entries
        context.anki_cards = []
        for entry in context.pleco_entries:
            anki_card = pleco_to_anki(entry, anki_export_parser)
            context.anki_cards.append(anki_card)
    elif hasattr(context, "pleco_entry"):
        # Convert single entry
        context.anki_card = pleco_to_anki(context.pleco_entry, anki_export_parser)
        # Also create anki_cards list for consistency
        context.anki_cards = [context.anki_card]
    else:
        raise ValueError("No Pleco entries found in context")


@then("I should get the following Anki card")
@then("I should get the following Anki cards")
def step_verify_anki_card(context):
    """Verify the converted Anki card(s) match expected values."""
    # Handle both single card and multiple cards scenarios
    if hasattr(context, "anki_cards"):
        # Multiple cards scenario
        actual_cards = context.anki_cards
    else:
        # Single card scenario - convert to list for uniform processing
        actual_cards = [context.anki_card]

    expected_rows = list(context.table)
    assert len(actual_cards) == len(expected_rows), f"Expected {len(expected_rows)} cards, got {len(actual_cards)}"

    for i, (actual_card, row) in enumerate(zip(actual_cards, expected_rows)):
        # Check required fields
        expected_pinyin = row["pinyin"]
        expected_simplified = row["simplified"]

        assert (
            actual_card.pinyin == expected_pinyin
        ), f"Card {i}: expected pinyin '{expected_pinyin}', got '{actual_card.pinyin}'"
        assert (
            actual_card.simplified == expected_simplified
        ), f"Card {i}: expected simplified '{expected_simplified}', got '{actual_card.simplified}'"

        # Check optional fields if present in the table
        if "meaning" in row:
            expected_meaning = row["meaning"]
            # Handle escaped newlines in expected meaning
            expected_meaning = expected_meaning.replace("\\n", "\n")
            assert (
                actual_card.meaning == expected_meaning
            ), f"Card {i}: expected meaning '{expected_meaning}', got '{actual_card.meaning}'"

        if "examples" in row:
            expected_examples = row["examples"]
            if expected_examples:
                # Convert list to newline-separated string for comparison
                actual_examples = "\n".join(actual_card.examples) if actual_card.examples else None
                # Handle escaped newlines in expected examples
                expected_examples = expected_examples.replace("\\n", "\n")
                assert actual_examples == expected_examples, (
                    f"Card {i}: expected examples '{expected_examples}', " f"got '{actual_examples}'"
                )

        if "structural_decomposition" in row:
            expected_structural_decomposition = row["structural_decomposition"]
            actual_structural_decomposition = actual_card.structural_decomposition
            assert actual_structural_decomposition == expected_structural_decomposition, (
                f"Card {i}: expected structural_decomposition '{expected_structural_decomposition}', "
                f"got '{actual_structural_decomposition}'"
            )


@then("the Anki card should have the following default values")
def step_verify_default_values(context):
    """Verify the Anki card has expected default values."""
    for row in context.table:
        field = row["field"]
        expected_value = row["value"]

        actual_value = getattr(context.anki_card, field)

        if expected_value == "None":
            assert actual_value is None, f"Expected {field} to be None, got {actual_value}"
        elif expected_value == "False":
            assert actual_value is False, f"Expected {field} to be False, got {actual_value}"
        else:
            assert str(actual_value) == expected_value, f"Expected {field} to be {expected_value}, got {actual_value}"


@then("I should get the following examples")
def step_verify_examples(context):
    """Verify that the converted Anki card has the expected examples."""
    if not hasattr(context, "anki_card"):
        raise ValueError("No Anki card found in context")

    # Get expected examples from the table
    expected_examples = []
    for row in context.table:
        example = row["example"]
        if example.strip():  # Only add non-empty examples
            expected_examples.append(example)

    # Get actual examples from the card
    actual_examples = context.anki_card.examples or []

    # Handle empty examples case
    if not expected_examples and not actual_examples:
        return  # Both are empty, test passes

    # Check if we have the expected number of examples
    assert len(actual_examples) == len(expected_examples), (
        f"Expected {len(expected_examples)} examples, got {len(actual_examples)}\n"
        f"Expected: {expected_examples}\n"
        f"Actual: {actual_examples}"
    )

    # Check each example
    for i, (expected, actual) in enumerate(zip(expected_examples, actual_examples)):
        assert actual == expected, f"Example {i+1} mismatch:\n" f"Expected: '{expected}'\n" f"Actual: '{actual}'"


# Step definitions for Anki export enhancement


@given('I have the following multi-character words in the Anki export containing "{character}"')
def step_have_anki_export_with_character(context, character):
    """Create mock Anki export data with multi-character words containing the character."""
    # Create an AnkiExportParser with mock data
    context.anki_parser = AnkiExportParser()
    context.anki_parser.cards = []

    for row in context.table:
        # Create mock AnkiCard from table data
        card = AnkiCard(
            notetype="Chinese",
            pinyin=row["pinyin"],
            characters=row["word"],
            audio="",
            definitions=row["meaning"],
        )
        context.anki_parser.cards.append(card)


@given('I have no multi-character words in the Anki export containing "{character}"')
def step_have_empty_anki_export(context, character):
    """Create empty AnkiExportParser (no words containing the character)."""
    context.anki_parser = AnkiExportParser()
    context.anki_parser.cards = []


@when("I convert the Pleco entry to an Anki card with Anki export enhancement")
def step_convert_with_anki_enhancement(context):
    """Convert Pleco entry to Anki card using the Anki export parser."""
    if hasattr(context, "pleco_entry"):
        context.anki_card = pleco_to_anki(context.pleco_entry, context.anki_parser)
    else:
        raise ValueError("No Pleco entry found in context")


@when("I convert them to Anki cards with Anki export enhancement")
def step_convert_multiple_with_anki_enhancement(context):
    """Convert multiple Pleco entries to Anki cards using the Anki export parser."""
    if hasattr(context, "pleco_entries"):
        context.anki_cards = []
        for entry in context.pleco_entries:
            anki_card = pleco_to_anki(entry, context.anki_parser)
            context.anki_cards.append(anki_card)
    else:
        raise ValueError("No Pleco entries found in context")


@then("I should get an Anki card with examples")
def step_verify_anki_card_examples(context):
    """Verify the converted Anki card has the expected examples."""
    if not hasattr(context, "anki_card"):
        raise ValueError("No Anki card found in context")

    # Get expected examples from the table
    expected_examples = []
    for row in context.table:
        example = row["example"]
        if example.strip():  # Only add non-empty examples
            expected_examples.append(example)

    # Get actual examples from the card
    actual_examples = context.anki_card.examples or []

    # Check if we have the expected number of examples
    assert len(actual_examples) == len(expected_examples), (
        f"Expected {len(expected_examples)} examples, got {len(actual_examples)}\n"
        f"Expected: {expected_examples}\n"
        f"Actual: {actual_examples}"
    )

    # Check each example
    for i, (expected, actual) in enumerate(zip(expected_examples, actual_examples)):
        assert actual == expected, f"Example {i+1} mismatch:\n" f"Expected: '{expected}'\n" f"Actual: '{actual}'"


@then("I should get an Anki card with no additional examples")
def step_verify_no_additional_examples(context):
    """Verify the Anki card has no additional examples from the export."""
    if not hasattr(context, "anki_card"):
        raise ValueError("No Anki card found in context")

    # For this test, we expect no examples or only examples from the original definition
    # Since we're not providing any examples in the Pleco definition in these scenarios,
    # we expect the examples list to be empty
    actual_examples = context.anki_card.examples or []

    # The card should have no examples (empty list or None)
    assert not actual_examples, f"Expected no additional examples, but got: {actual_examples}"


@then("I should get an Anki card with no additional examples from the export")
def step_verify_no_export_examples(context):
    """Verify multi-character words don't get additional examples from export."""
    if not hasattr(context, "anki_card"):
        raise ValueError("No Anki card found in context")

    # Multi-character words should not get additional examples from the export
    # They should only have examples from their original Pleco definition
    actual_examples = context.anki_card.examples or []

    # Since we didn't provide examples in the definition, should be empty
    assert not actual_examples, f"Expected no examples for multi-character word, but got: {actual_examples}"
