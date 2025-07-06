"""Behave environment setup for BDD tests."""

import os
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
