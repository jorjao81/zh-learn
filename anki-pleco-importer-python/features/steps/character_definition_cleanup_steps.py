"""Step definitions for character definition cleanup feature."""

from behave import given, when, then
from anki_pleco_importer.chinese import clean_character_definition


@given("I have the following test dictionary data")
def step_given_test_dictionary_data(context):
    """Set up test dictionary data."""
    context.test_data = {}
    for row in context.table:
        chinese = row["Chinese"]
        pinyin = row["Pinyin"]
        definition = row["Definition"]
        context.test_data[chinese] = {"pinyin": pinyin, "definition": definition}


@given('I have a character "{character}" with definition "{definition}"')
def step_given_character_with_definition(context, character, definition):
    """Set up a single character with definition."""
    if not hasattr(context, "test_data"):
        context.test_data = {}
    context.test_data[character] = {"pinyin": "", "definition": definition}


@when("I process the character definitions for cleanup")
def step_when_process_definitions_for_cleanup(context):
    """Process character definitions through cleanup."""
    context.cleaned_data = {}
    for character, data in context.test_data.items():
        cleaned_definition = clean_character_definition(data["definition"])
        context.cleaned_data[character] = cleaned_definition


@then('the definition for "{character}" should be "{expected_definition}"')
def step_then_definition_should_be(context, character, expected_definition):
    """Check that the cleaned definition matches expected result."""
    actual_definition = context.cleaned_data[character]
    assert actual_definition == expected_definition, (
        f"Expected definition for '{character}': '{expected_definition}', " f"but got: '{actual_definition}'"
    )


@then('the definition for "{character}" should be ""')
def step_then_definition_should_be_empty(context, character):
    """Check that the cleaned definition is empty."""
    actual_definition = context.cleaned_data[character]
    assert actual_definition == "", f"Expected empty definition for '{character}', but got: '{actual_definition}'"
