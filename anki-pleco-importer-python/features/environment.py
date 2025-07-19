"""Behave environment setup for BDD tests."""

import tempfile
from pathlib import Path


def before_all(context):
    """Set up test environment before all tests."""
    context.temp_dir = tempfile.mkdtemp()
    context.test_files_dir = Path(context.temp_dir)


def after_all(context):
    """Clean up test environment after all tests."""
    import shutil

    if hasattr(context, "temp_dir"):
        shutil.rmtree(context.temp_dir, ignore_errors=True)


def before_scenario(context, scenario):
    """Set up before each scenario."""
    context.input_file = None
    context.output_file = None
    context.result = None
    context.error = None
    context.google_drive_files = []


def before_step(context, step):
    """Handle special step setups."""
    # Handle Google Drive download commands by mocking the service
    if step.step_type == "when" and "download-from-drive" in step.name:
        from unittest.mock import patch
        from anki_pleco_importer.google_drive import GoogleDriveError

        # Set up the mock for the download function
        def mock_download_latest_flash_file(output_dir="."):
            # Filter flash files and sort by creation time
            flash_files = [f for f in context.google_drive_files if f["name"].startswith("flash-")]
            if flash_files:
                # Sort by creation time (most recent first)
                flash_files.sort(key=lambda f: f["createdTime"], reverse=True)
                latest_file = flash_files[0]
                return f"{output_dir}/{latest_file['name']}"
            else:
                raise GoogleDriveError("No files starting with 'flash-' found in Google Drive")

        # Apply the patch
        patcher = patch(
            "anki_pleco_importer.cli.download_latest_flash_file", side_effect=mock_download_latest_flash_file
        )
        context.google_drive_patcher = patcher
        patcher.start()


def after_step(context, step):
    """Clean up after step."""
    # Clean up Google Drive patches
    if hasattr(context, "google_drive_patcher"):
        context.google_drive_patcher.stop()
        delattr(context, "google_drive_patcher")
