"""Command line interface for Anki Pleco Importer."""

import click
import re
from pathlib import Path

from .parser import PlecoTSVParser
from .models import pleco_to_anki


def format_html_for_terminal(text: str) -> str:
    """Convert simple HTML tags to click formatting for terminal output."""

    # Replace <b>...</b> with click's bold formatting
    def replace_bold(match: re.Match[str]) -> str:
        content = match.group(1)
        return click.style(content, bold=True)

    # Handle bold tags (case insensitive)
    formatted = re.sub(r"<b>(.*?)</b>", replace_bold, text, flags=re.IGNORECASE)

    # Also handle self-closing bold tags if any
    formatted = re.sub(r"<B>(.*?)</B>", replace_bold, formatted)

    return formatted


def format_meaning_box(meaning: str) -> str:
    """Format meaning text in a multi-line box for better readability."""
    # Format HTML first
    formatted_meaning = format_html_for_terminal(meaning)

    # Split into lines
    lines = formatted_meaning.split("\n")

    # Calculate the maximum width needed (considering ANSI escape codes don't count for display width)
    max_width = 0
    display_lines = []
    for line in lines:
        # Remove ANSI escape codes to calculate actual display width
        display_line = re.sub(r"\x1b\[[0-9;]*m", "", line)
        display_lines.append(display_line)
        max_width = max(max_width, len(display_line))

    # Add some padding
    box_width = max_width + 4

    # Create the box
    top_border = "    ┌" + "─" * (box_width - 2) + "┐"
    bottom_border = "    └" + "─" * (box_width - 2) + "┘"

    # Create the content lines
    content_lines = []
    for i, line in enumerate(lines):
        display_line = display_lines[i]
        padding = box_width - 4 - len(display_line)
        content_lines.append(f"    │ {line}{' ' * padding} │")

    # Combine everything
    result = [top_border] + content_lines + [bottom_border]
    return "\n".join(result)


@click.command()
@click.argument("tsv_file", type=click.Path(exists=True, path_type=Path), required=False)
@click.version_option()
def main(tsv_file: Path) -> None:
    """Convert Pleco flashcard exports to Anki-compatible format."""
    if tsv_file:
        parser = PlecoTSVParser()
        try:
            collection = parser.parse_file(tsv_file)
            click.echo(click.style(f"Parsed {len(collection)} entries from {tsv_file}:", fg="green", bold=True))
            click.echo()

            for i, entry in enumerate(collection, 1):
                anki_card = pleco_to_anki(entry)
                click.echo(click.style(f"{i:2d}. {anki_card.simplified} ({anki_card.pinyin})", fg="cyan", bold=True))
                click.echo(f"    {click.style('Meaning:', fg='yellow', bold=True)}")
                meaning_box = format_meaning_box(anki_card.meaning)
                click.echo(meaning_box)
                click.echo()

        except Exception as e:
            click.echo(f"Error parsing file: {e}", err=True)
            raise click.Abort()
    else:
        click.echo("Anki Pleco Importer")
        click.echo("Usage: anki-pleco-importer <tsv_file>")


if __name__ == "__main__":
    main()
