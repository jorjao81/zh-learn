"""Command line interface for Anki Pleco Importer."""

import click
import re
from pathlib import Path
from typing import List

from .parser import PlecoTSVParser
from .models import pleco_to_anki


def format_html_for_terminal(text: str) -> str:
    """Convert simple HTML tags to click formatting for terminal output."""

    # Replace <b>...</b> with click's bold formatting
    def replace_bold(match: re.Match[str]) -> str:
        content = match.group(1)
        return click.style(content, bold=True)

    # Replace <span color="red">...</span> with click's red color formatting
    def replace_red_span(match: re.Match[str]) -> str:
        content = match.group(1)
        return click.style(content, fg="red")

    # Handle bold tags (case insensitive)
    formatted = re.sub(r"<b>(.*?)</b>", replace_bold, text, flags=re.IGNORECASE)

    # Also handle self-closing bold tags if any
    formatted = re.sub(r"<B>(.*?)</B>", replace_bold, formatted)

    # Handle red span tags (case insensitive)
    formatted = re.sub(r'<span\s+color="red">(.*?)</span>', replace_red_span, formatted, flags=re.IGNORECASE)

    return formatted


def wrap_text_with_ansi(text: str, width: int) -> List[str]:
    """Wrap text at specified width while preserving ANSI escape codes."""
    # Split text into segments of ANSI codes and regular text
    segments = re.split(r"(\x1b\[[0-9;]*m)", text)

    wrapped_lines = []
    current_line = ""
    current_display_width = 0

    for segment in segments:
        if re.match(r"\x1b\[[0-9;]*m", segment):
            # This is an ANSI escape code, add it without counting width
            current_line += segment
        else:
            # This is regular text, wrap it
            while segment:
                remaining_width = width - current_display_width
                if remaining_width <= 0:
                    # Start a new line
                    wrapped_lines.append(current_line)
                    current_line = ""
                    current_display_width = 0
                    remaining_width = width

                if len(segment) <= remaining_width:
                    # Entire segment fits
                    current_line += segment
                    current_display_width += len(segment)
                    break
                else:
                    # Find the last space within the remaining width
                    break_point = remaining_width
                    space_pos = segment.rfind(" ", 0, break_point)

                    if space_pos != -1 and space_pos > 0:
                        # Break at the space
                        current_line += segment[:space_pos]
                        wrapped_lines.append(current_line)
                        current_line = ""
                        current_display_width = 0
                        segment = segment[space_pos + 1 :]  # Skip the space
                    else:
                        # No space found, force break at width
                        current_line += segment[:remaining_width]
                        wrapped_lines.append(current_line)
                        current_line = ""
                        current_display_width = 0
                        segment = segment[remaining_width:]

    # Add any remaining content
    if current_line:
        wrapped_lines.append(current_line)

    return wrapped_lines


def format_meaning_box(meaning: str) -> str:
    """Format meaning text in a multi-line box for better readability."""
    # Format HTML first
    formatted_meaning = format_html_for_terminal(meaning)

    # Split into lines and wrap each line at 80 characters
    lines = formatted_meaning.split("\n")
    wrapped_lines = []

    for line in lines:
        if line.strip():  # Only wrap non-empty lines
            wrapped_lines.extend(wrap_text_with_ansi(line, 80))
        else:
            wrapped_lines.append(line)  # Preserve empty lines

    # Calculate the maximum display width (excluding ANSI codes)
    max_width = 0
    display_lines = []
    for line in wrapped_lines:
        # Remove ANSI escape codes to calculate actual display width
        display_line = re.sub(r"\x1b\[[0-9;]*m", "", line)
        display_lines.append(display_line)
        max_width = max(max_width, len(display_line))

    # Ensure minimum box width and add padding
    # Since we wrap at 80 characters, the box should be exactly 84 characters (80 + 4 for padding)
    box_width = 84

    # Create the box
    top_border = "    ┌" + "─" * (box_width - 2) + "┐"
    bottom_border = "    └" + "─" * (box_width - 2) + "┘"

    # Create the content lines
    content_lines = []
    for i, line in enumerate(wrapped_lines):
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
                click.echo(click.style(f"{i:2d}. {anki_card.simplified} ", fg="cyan", bold=True) + anki_card.pinyin)
                click.echo(f"    {click.style('Meaning:', fg='yellow', bold=True)}")
                meaning_box = format_meaning_box(anki_card.meaning)
                click.echo(meaning_box)

                if anki_card.semantic_component:
                    click.echo(f"    {click.style('Components:', fg='magenta', bold=True)}")
                    component_box = format_meaning_box(anki_card.semantic_component)
                    click.echo(component_box)

                click.echo()

        except Exception as e:
            click.echo(f"Error parsing file: {e}", err=True)
            raise click.Abort()
    else:
        click.echo("Anki Pleco Importer")
        click.echo("Usage: anki-pleco-importer <tsv_file>")


if __name__ == "__main__":
    main()
