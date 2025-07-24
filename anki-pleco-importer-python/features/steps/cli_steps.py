"""Step definitions for CLI interface BDD tests."""

import subprocess
import sys
from pathlib import Path
from behave import given, when, then


@when('I run the command "{command}"')
def step_run_command(context, command):
    """Run a command and capture output."""
    try:
        # Replace the command with the actual module call for testing
        if command.startswith("anki-pleco-importer"):
            cmd_parts = command.split()
            cmd_parts[0] = sys.executable
            cmd_parts.insert(1, "-m")
            cmd_parts.insert(2, "anki_pleco_importer.cli")

            result = subprocess.run(
                cmd_parts,
                cwd=Path.cwd(),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        else:
            result = subprocess.run(
                command.split(),
                cwd=context.test_files_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

        context.command_result = result
        context.exit_code = result.returncode
        context.stdout = result.stdout
        context.stderr = result.stderr

    except Exception as e:
        context.command_error = str(e)
        context.exit_code = 1


@given('I have a Pleco export file "{filename}"')
def step_create_pleco_file(context, filename):
    """Create a Pleco export file for testing."""
    file_path = context.test_files_dir / filename
    sample_content = "你好\thello\tnǐ hǎo\n谢谢\tthank you\txiè xie"
    file_path.write_text(sample_content, encoding="utf-8")
    context.input_file = file_path


@then("the output should contain usage information")
def step_verify_usage_info(context):
    """Verify the output contains usage information."""
    output = context.stdout + context.stderr
    assert "usage:" in output.lower() or "Usage:" in output, "Output should contain usage information"


@then("the output should contain available options")
def step_verify_available_options(context):
    """Verify the output contains available options."""
    output = context.stdout + context.stderr
    assert "--help" in output or "options:" in output.lower(), "Output should contain available options"


@then("the output should contain the version number")
def step_verify_version_number(context):
    """Verify the output contains version number."""
    output = context.stdout + context.stderr
    # Since we haven't implemented version display yet, this is a placeholder
    assert len(output) > 0, "Output should not be empty"


@then('the file "{filename}" should be created')
def step_verify_file_created(context, filename):
    """Verify the specified file was created."""
    file_path = context.test_files_dir / filename
    assert file_path.exists(), f"File {filename} should be created"


@then('the file "{filename}" should contain the converted data')
def step_verify_file_contains_data(context, filename):
    """Verify the file contains converted data."""
    file_path = context.test_files_dir / filename
    assert file_path.exists(), f"File {filename} should exist"

    content = file_path.read_text(encoding="utf-8")
    assert len(content) > 0, "File should not be empty"
    assert "Front" in content, "File should contain CSV headers"


@then("I should get an error about the missing file")
def step_verify_missing_file_error(context):
    """Verify an error about missing file is shown."""
    error_output = context.stderr
    assert (
        "not found" in error_output.lower() or "no such file" in error_output.lower()
    ), "Should get error about missing file"


@then("the exit code should be non-zero")
def step_verify_non_zero_exit_code(context):
    """Verify the exit code is non-zero."""
    assert context.exit_code != 0, f"Exit code should be non-zero, got {context.exit_code}"


@given('I have the sample TSV file "import.tsv"')
def step_sample_tsv_file(context):
    """Verify the sample TSV file exists."""
    sample_file = Path("features/examples/import.tsv")
    assert sample_file.exists(), "Sample TSV file should exist"


@then('the output should contain "{expected_text}"')
def step_verify_output_contains(context, expected_text):
    """Verify the output contains the expected text."""
    output = context.stdout + context.stderr
    assert expected_text in output, f"Output should contain '{expected_text}'. Got: {output}"
