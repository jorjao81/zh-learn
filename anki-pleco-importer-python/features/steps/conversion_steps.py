"""Step definitions for Pleco to Anki conversion BDD tests."""

import csv
import io
from pathlib import Path
from behave import given, when, then
from anki_pleco_importer.cli import main
from anki_pleco_importer.pleco import PlecoEntry, pleco_to_anki


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
        entry = PlecoEntry(
            chinese=row["chinese"],
            pinyin=row["pinyin"], 
            definition=row["definition"]
        )
        context.pleco_entries.append(entry)
    
    # For backward compatibility with single entry scenarios
    if len(context.pleco_entries) == 1:
        context.pleco_entry = context.pleco_entries[0]


@given('I have a Pleco entry with chinese "{chinese}", pinyin "{pinyin}", and definition "{definition}"')
def step_have_pleco_entry_with_values(context, chinese, pinyin, definition):
    """Create a Pleco entry with specific values."""
    context.pleco_entry = PlecoEntry(
        chinese=chinese,
        pinyin=pinyin,
        definition=definition
    )


@when("I convert them to Anki cards")
@when("I convert it to an Anki card")
def step_convert_to_anki(context):
    """Convert Pleco entries to Anki cards (handles both single and multiple)."""
    if hasattr(context, 'pleco_entries'):
        # Convert multiple entries
        context.anki_cards = []
        for entry in context.pleco_entries:
            anki_card = pleco_to_anki(entry)
            context.anki_cards.append(anki_card)
    elif hasattr(context, 'pleco_entry'):
        # Convert single entry
        context.anki_card = pleco_to_anki(context.pleco_entry)
        # Also create anki_cards list for consistency
        context.anki_cards = [context.anki_card]
    else:
        raise ValueError("No Pleco entries found in context")


@then("I should get the following Anki card")
@then("I should get the following Anki cards")
def step_verify_anki_card(context):
    """Verify the converted Anki card(s) match expected values."""
    # Handle both single card and multiple cards scenarios
    if hasattr(context, 'anki_cards'):
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
        
        assert actual_card.pinyin == expected_pinyin, f"Card {i}: expected pinyin '{expected_pinyin}', got '{actual_card.pinyin}'"
        assert actual_card.simplified == expected_simplified, f"Card {i}: expected simplified '{expected_simplified}', got '{actual_card.simplified}'"
        
        # Check optional fields if present in the table
        if "meaning" in row:
            expected_meaning = row["meaning"]
            # Handle escaped newlines in expected meaning
            expected_meaning = expected_meaning.replace('\\n', '\n')
            assert actual_card.meaning == expected_meaning, f"Card {i}: expected meaning '{expected_meaning}', got '{actual_card.meaning}'"
        
        if "examples" in row:
            expected_examples = row["examples"]
            if expected_examples:
                # Convert list to newline-separated string for comparison
                actual_examples = "\n".join(actual_card.examples) if actual_card.examples else None
                # Handle escaped newlines in expected examples
                expected_examples = expected_examples.replace('\\n', '\n')
                assert actual_examples == expected_examples, f"Card {i}: expected examples '{expected_examples}', got '{actual_examples}'"
        
        if "semantic_component" in row:
            expected_semantic_component = row["semantic_component"]
            actual_semantic_component = actual_card.semantic_component
            assert actual_semantic_component == expected_semantic_component, f"Card {i}: expected semantic_component '{expected_semantic_component}', got '{actual_semantic_component}'"


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
