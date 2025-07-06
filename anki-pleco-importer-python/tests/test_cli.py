"""Tests for the CLI module."""

import pytest
from click.testing import CliRunner
from anki_pleco_importer.cli import main


def test_cli_help():
    """Test that CLI help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Convert Pleco flashcard exports" in result.output


def test_cli_version():
    """Test that CLI version works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0


def test_cli_main():
    """Test that CLI main function works."""
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Coming soon" in result.output
