"""Step definitions for Google Drive download feature."""

from behave import given, then
from unittest.mock import patch


@given("I have Google Drive API credentials configured")
def step_google_drive_credentials_configured(context):
    """Mock Google Drive credentials configuration."""
    # Create a mock credentials file
    context.mock_credentials = True


@given("my Google Drive contains the following files")
def step_google_drive_contains_files(context):
    """Mock Google Drive files from table."""
    context.google_drive_files = []
    for row in context.table:
        context.google_drive_files.append(
            {
                "id": f"file_{row['filename']}",
                "name": row["filename"],
                "createdTime": f"{row['upload_date'].replace(' ', 'T')}Z",
                "modifiedTime": f"{row['upload_date'].replace(' ', 'T')}Z",
            }
        )


@given("my Google Drive contains only the following files")
def step_google_drive_contains_only_files(context):
    """Mock Google Drive files from table (only these files)."""
    step_google_drive_contains_files(context)


def mock_google_drive_for_command(context, command_args):
    """Helper function to mock Google Drive for commands."""
    with patch("anki_pleco_importer.google_drive.download_latest_flash_file") as mock_download:
        # Filter flash files and sort by creation time
        flash_files = [f for f in context.google_drive_files if f["name"].startswith("flash-")]
        if flash_files:
            # Sort by creation time (most recent first)
            flash_files.sort(key=lambda f: f["createdTime"], reverse=True)
            latest_file = flash_files[0]
            # Mock successful download
            output_dir = (
                "." if "--output-dir" not in command_args else command_args[command_args.index("--output-dir") + 1]
            )
            mock_download.return_value = f"{output_dir}/{latest_file['name']}"
        else:
            # Mock error for no files found
            from anki_pleco_importer.google_drive import GoogleDriveError

            mock_download.side_effect = GoogleDriveError("No files starting with 'flash-' found in Google Drive")

        # Import and run the CLI
        from anki_pleco_importer.cli import cli
        from click.testing import CliRunner

        runner = CliRunner()
        context.result = runner.invoke(cli, command_args)


@then('the file "flash-latest-2023.txt" should be downloaded to the current directory')
def step_file_downloaded_to_current_directory(context):
    """Verify file was downloaded to current directory."""
    assert context.exit_code == 0
    output = context.stdout + context.stderr
    assert "Downloaded: flash-latest-2023.txt" in output


@then('the file "flash-latest-2023.txt" should be downloaded to "/tmp/downloads/"')
def step_file_downloaded_to_output_directory(context):
    """Verify file was downloaded to specified directory."""
    assert context.exit_code == 0
    output = context.stdout + context.stderr
    assert "Downloaded: flash-latest-2023.txt to /tmp/downloads/" in output


@then("the command should exit with error code 1")
def step_command_exits_with_error(context):
    """Verify command exits with error."""
    assert context.exit_code == 1
