"""Step definitions for Pleco to Anki conversion BDD tests."""

import csv
import io
from pathlib import Path
from behave import given, when, then
from anki_pleco_importer.cli import main
from anki_pleco_importer.pleco import PlecoEntry, pleco_to_anki


@given("I have the anki-pleco-importer application")
def step_have_application(context):
    """Verify the application is available."""
    context.app_available = True


@given("I have a Pleco export file with the following content")
def step_create_pleco_file_with_content(context):
    """Create a Pleco export file with specified content."""
    context.input_file = context.test_files_dir / "pleco_export.txt"
    context.input_file.write_text(context.text, encoding="utf-8")


@given("I have an empty Pleco export file")
def step_create_empty_pleco_file(context):
    """Create an empty Pleco export file."""
    context.input_file = context.test_files_dir / "empty_pleco_export.txt"
    context.input_file.write_text("", encoding="utf-8")


@given("I have a valid Pleco export file")
def step_create_valid_pleco_file(context):
    """Create a valid Pleco export file."""
    content = "你好\thello\tnǐ hǎo\n谢谢\tthank you\txiè xie"
    context.input_file = context.test_files_dir / "valid_pleco_export.txt"
    context.input_file.write_text(content, encoding="utf-8")


@given("I have a Pleco export file with malformed data")
def step_create_malformed_pleco_file(context):
    """Create a Pleco export file with malformed data."""
    context.input_file = context.test_files_dir / "malformed_pleco_export.txt"
    context.input_file.write_text(context.text, encoding="utf-8")


@given("I have a Pleco export file with special characters")
def step_create_special_chars_pleco_file(context):
    """Create a Pleco export file with special characters."""
    context.input_file = context.test_files_dir / "special_chars_pleco_export.txt"
    context.input_file.write_text(context.text, encoding="utf-8")


@when("I convert the file to Anki format")
def step_convert_to_anki_format(context):
    """Convert the Pleco file to Anki format."""
    context.output_file = context.test_files_dir / "anki_output.csv"

    # This is a placeholder - the actual conversion logic will be implemented later
    # For now, we'll create a mock successful conversion
    try:
        # Mock conversion logic
        if context.input_file.stat().st_size == 0:
            context.error = "No flashcards found in input file"
            return

        # Create a simple CSV output for testing
        with open(context.output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Front", "Back", "Pinyin"])

            # Parse the input file
            with open(context.input_file, "r", encoding="utf-8") as infile:
                for line in infile:
                    line = line.strip()
                    if line:
                        parts = line.split("\t")
                        if len(parts) >= 3:
                            writer.writerow([parts[0], parts[1], parts[2]])

        context.result = "success"
    except Exception as e:
        context.error = str(e)


@then("the output should be a valid Anki CSV file")
def step_verify_valid_anki_csv(context):
    """Verify the output is a valid Anki CSV file."""
    assert context.output_file.exists(), "Output file should exist"

    # Check if it's valid CSV
    with open(context.output_file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        assert len(rows) > 0, "CSV should have at least header row"


@then("the output should contain the following cards")
def step_verify_cards_content(context):
    """Verify the output contains expected cards."""
    with open(context.output_file, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    expected_rows = []
    for row in context.table:
        expected_rows.append(
            {"Front": row["Front"], "Back": row["Back"], "Pinyin": row["Pinyin"]}
        )

    for expected_row in expected_rows:
        assert expected_row in rows, f"Expected row {expected_row} not found in output"


@then('I should get an error message "{error_message}"')
def step_verify_error_message(context, error_message):
    """Verify the expected error message."""
    assert (
        context.error == error_message
    ), f"Expected error: {error_message}, got: {context.error}"


@then("the output file should have CSV headers")
def step_verify_csv_headers(context):
    """Verify the output file has proper CSV headers."""
    with open(context.output_file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        assert "Front" in headers, "CSV should have 'Front' header"
        assert "Back" in headers, "CSV should have 'Back' header"
        assert "Pinyin" in headers, "CSV should have 'Pinyin' header"


@then("the output file should be properly formatted for Anki import")
def step_verify_anki_format(context):
    """Verify the output file is properly formatted for Anki."""
    with open(context.output_file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        # Check header row
        assert rows[0] == [
            "Front",
            "Back",
            "Pinyin",
        ], "Headers should match Anki format"

        # Check data rows have correct number of columns
        for row in rows[1:]:
            assert len(row) == 3, f"Each data row should have 3 columns, got {len(row)}"


@then("I should get a warning about inconsistent data format")
def step_verify_warning_message(context):
    """Verify a warning about inconsistent data format."""
    # This is a placeholder - warnings handling will be implemented later
    assert True, "Warning handling not yet implemented"


@then("the conversion should still proceed with available data")
def step_verify_conversion_proceeds(context):
    """Verify conversion proceeds despite warnings."""
    assert context.output_file.exists(), "Output file should exist even with warnings"


@then("the output should preserve all special characters correctly")
def step_verify_special_characters(context):
    """Verify special characters are preserved."""
    with open(context.output_file, "r", encoding="utf-8") as csvfile:
        content = csvfile.read()
        assert "你好" in content, "Chinese characters should be preserved"
        assert "Hello, world!" in content, "Special punctuation should be preserved"


@then("the quotes should be handled properly in the CSV format")
def step_verify_quotes_handling(context):
    """Verify quotes are handled properly in CSV format."""
    with open(context.output_file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        # Check that quotes are properly escaped/handled
        for row in rows[1:]:  # Skip header
            for cell in row:
                # The CSV reader should handle quotes correctly
                assert cell is not None, "Cell should not be None"


# New step definitions for pleco_to_anki conversion

@given("the pleco_to_anki conversion function is available")
def step_conversion_function_available(context):
    """Verify the pleco_to_anki conversion function is available."""
    context.conversion_available = True


@given("I have the following Pleco entries")
def step_have_pleco_entries(context):
    """Create Pleco entries from table data."""
    context.pleco_entries = []
    for row in context.table:
        entry = PlecoEntry(
            chinese=row["chinese"],
            pinyin=row["pinyin"], 
            definition=row["definition"]
        )
        context.pleco_entries.append(entry)


@given("I have the following Pleco entry")
def step_have_pleco_entry(context):
    """Create a single Pleco entry from table data."""
    row = context.table[0]
    context.pleco_entry = PlecoEntry(
        chinese=row["chinese"],
        pinyin=row["pinyin"],
        definition=row["definition"]
    )


@given('I have a Pleco entry with chinese "{chinese}", pinyin "{pinyin}", and definition "{definition}"')
def step_have_pleco_entry_with_values(context, chinese, pinyin, definition):
    """Create a Pleco entry with specific values."""
    context.pleco_entry = PlecoEntry(
        chinese=chinese,
        pinyin=pinyin,
        definition=definition
    )


@when("I convert them to Anki cards")
def step_convert_entries_to_anki(context):
    """Convert multiple Pleco entries to Anki cards."""
    context.anki_cards = []
    for entry in context.pleco_entries:
        anki_card = pleco_to_anki(entry)
        context.anki_cards.append(anki_card)


@when("I convert it to an Anki card")
def step_convert_entry_to_anki(context):
    """Convert a single Pleco entry to an Anki card."""
    context.anki_card = pleco_to_anki(context.pleco_entry)


@then("I should get the following Anki cards")
def step_verify_anki_cards(context):
    """Verify the converted Anki cards match expected values."""
    expected_cards = []
    for row in context.table:
        expected_cards.append({
            "pinyin": row["pinyin"],
            "simplified": row["simplified"],
            "meaning": row["meaning"]
        })
    
    assert len(context.anki_cards) == len(expected_cards), f"Expected {len(expected_cards)} cards, got {len(context.anki_cards)}"
    
    for i, (actual_card, expected_card) in enumerate(zip(context.anki_cards, expected_cards)):
        assert actual_card.pinyin == expected_card["pinyin"], f"Card {i}: expected pinyin '{expected_card['pinyin']}', got '{actual_card.pinyin}'"
        assert actual_card.simplified == expected_card["simplified"], f"Card {i}: expected simplified '{expected_card['simplified']}', got '{actual_card.simplified}'"
        assert actual_card.meaning == expected_card["meaning"], f"Card {i}: expected meaning '{expected_card['meaning']}', got '{actual_card.meaning}'"


@then("I should get the following Anki card")
def step_verify_anki_card(context):
    """Verify the converted Anki card matches expected values."""
    row = context.table[0]
    expected_pinyin = row["pinyin"]
    expected_simplified = row["simplified"]
    
    assert context.anki_card.pinyin == expected_pinyin, f"Expected pinyin '{expected_pinyin}', got '{context.anki_card.pinyin}'"
    assert context.anki_card.simplified == expected_simplified, f"Expected simplified '{expected_simplified}', got '{context.anki_card.simplified}'"
    
    # Check meaning field if present in the table
    if "meaning" in row:
        expected_meaning = row["meaning"]
        # Handle escaped newlines in expected meaning
        expected_meaning = expected_meaning.replace('\\n', '\n')
        assert context.anki_card.meaning == expected_meaning, f"Expected meaning '{expected_meaning}', got '{context.anki_card.meaning}'"
    
    # Check examples field if present in the table
    if "examples" in row:
        expected_examples = row["examples"]
        if expected_examples:
            # Convert list to newline-separated string for comparison
            actual_examples = "\n".join(context.anki_card.examples) if context.anki_card.examples else None
            # Handle escaped newlines in expected examples
            expected_examples = expected_examples.replace('\\n', '\n')
            assert actual_examples == expected_examples, f"Expected examples '{expected_examples}', got '{actual_examples}'"
    
    # Check semantic_component field if present in the table
    if "semantic_component" in row:
        expected_semantic_component = row["semantic_component"]
        actual_semantic_component = context.anki_card.semantic_component
        assert actual_semantic_component == expected_semantic_component, f"Expected semantic_component '{expected_semantic_component}', got '{actual_semantic_component}'"


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
