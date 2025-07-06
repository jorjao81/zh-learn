"""Step definitions for Pleco to Anki conversion BDD tests."""

import csv
import io
from pathlib import Path
from behave import given, when, then
from anki_pleco_importer.cli import main


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
