"""Command line interface for Anki Pleco Importer."""

import click
import re
import pandas as pd
import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional

from .parser import PlecoTSVParser
from .pleco import pleco_to_anki
from .audio import MultiProviderAudioGenerator


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


def load_audio_config(config_file: Optional[str] = None, verbose: bool = False) -> Dict[str, Dict[str, Any]]:
    """Load audio configuration from file or environment variables."""
    config = {}

    # Determine config file to use
    if config_file is None:
        # Try default audio-config.json in current directory
        default_config = "audio-config.json"
        if os.path.exists(default_config):
            config_file = default_config

    # Try to load from config file first
    if config_file and os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                file_config = json.load(f)
                config.update(file_config.get("audio", {}))
            if verbose:
                click.echo(f"Loaded audio config from: {config_file}")
        except Exception as e:
            click.echo(f"Warning: Failed to load config file {config_file}: {e}", err=True)

    # Load from environment variables (override file config)
    env_config = {
        "forvo": {"api_key": os.getenv("FORVO_API_KEY")},
    }

    # Merge environment config with file config
    for provider, provider_config in env_config.items():
        if provider not in config:
            config[provider] = {}
        config[provider].update({k: v for k, v in provider_config.items() if v is not None})

    return config


@click.command()
@click.argument("tsv_file", type=click.Path(exists=True, path_type=Path), required=False)
@click.option("--audio", is_flag=True, help="Generate pronunciation audio files")
@click.option(
    "--audio-providers",
    default="forvo",
    help="Audio provider (only Forvo supported for high-quality human pronunciation)",
)
@click.option(
    "--audio-config",
    type=click.Path(exists=True),
    help="Path to audio configuration JSON file (default: audio-config.json if exists)",
)
@click.option("--audio-cache-dir", default="audio_cache", help="Directory to cache audio files")
@click.option("--audio-dest-dir", type=click.Path(), help="Directory to copy selected audio files to")
@click.option("--dry-run", is_flag=True, help="Show what would be done without making changes")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.version_option()
def main(
    tsv_file: Path,
    audio: bool,
    audio_providers: str,
    audio_config: Optional[str],
    audio_cache_dir: str,
    audio_dest_dir: Optional[str],
    dry_run: bool,
    verbose: bool,
) -> None:
    """Convert Pleco flashcard exports to Anki-compatible format."""

    # Configure logging level
    import logging

    if verbose:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    if tsv_file:
        parser = PlecoTSVParser()

        # Initialize audio generation if requested
        audio_generator = None
        if audio:
            try:
                config = load_audio_config(audio_config, verbose)
                providers = [p.strip() for p in audio_providers.split(",")]

                audio_generator = MultiProviderAudioGenerator(
                    providers=providers, config=config, cache_dir=audio_cache_dir
                )

                available_providers = audio_generator.get_available_providers()
                if available_providers:
                    click.echo(click.style(f"Audio providers available: {', '.join(available_providers)}", fg="green"))
                else:
                    click.echo(click.style("Warning: No audio providers available", fg="yellow"))
                    # Keep audio_generator to track skipped words even when no providers available

            except Exception as e:
                click.echo(click.style(f"Warning: Failed to initialize audio generation: {e}", fg="yellow"))
                audio_generator = None

        # Create audio destination directory if specified
        if audio_dest_dir and not dry_run:
            try:
                Path(audio_dest_dir).mkdir(parents=True, exist_ok=True)
                if verbose:
                    click.echo(f"Audio destination directory: {audio_dest_dir}")
            except Exception as e:
                click.echo(click.style(f"Warning: Failed to create audio destination directory: {e}", fg="yellow"))
                audio_dest_dir = None

        try:
            collection = parser.parse_file(tsv_file)
            click.echo(click.style(f"Parsed {len(collection)} entries from {tsv_file}:", fg="green", bold=True))
            click.echo()

            anki_cards = []
            for i, entry in enumerate(collection, 1):
                anki_card = pleco_to_anki(entry)

                # Generate audio if requested and not in dry-run mode
                if audio_generator and not dry_run:
                    try:
                        if verbose:
                            click.echo(f"    Generating audio for '{anki_card.simplified}'...")

                        audio_file = audio_generator.generate_audio(anki_card.simplified)
                        if audio_file:
                            anki_card.pronunciation = audio_file
                            if verbose:
                                click.echo(f"    Audio saved to: {audio_file}")
                            
                            # Copy to destination directory if specified
                            if audio_dest_dir:
                                try:
                                    audio_filename = Path(audio_file).name
                                    dest_path = Path(audio_dest_dir) / audio_filename
                                    shutil.copy2(audio_file, dest_path)
                                    if verbose:
                                        click.echo(f"    Audio copied to: {dest_path}")
                                except Exception as copy_error:
                                    click.echo(click.style(f"    Warning: Failed to copy audio to destination: {copy_error}", fg="yellow"))
                        elif verbose:
                            click.echo(f"    No audio generated for '{anki_card.simplified}'")

                    except Exception as e:
                        if verbose:
                            click.echo(f"    Audio generation failed for '{anki_card.simplified}': {e}")

                anki_cards.append(anki_card)

                # Display card information
                audio_indicator = " 🔊" if anki_card.pronunciation else ""
                click.echo(
                    click.style(f"{i:2d}. {anki_card.simplified} ", fg="cyan", bold=True)
                    + anki_card.pinyin
                    + audio_indicator
                )

                if verbose and anki_card.pronunciation:
                    click.echo(f"    {click.style('Audio:', fg='blue', bold=True)} {anki_card.pronunciation}")

                click.echo(f"    {click.style('Meaning:', fg='yellow', bold=True)}")
                meaning_box = format_meaning_box(anki_card.meaning)
                click.echo(meaning_box)

                if anki_card.examples:
                    click.echo(f"    {click.style('Examples:', fg='green', bold=True)}")
                    examples_text = " ; ".join(anki_card.examples)
                    examples_box = format_meaning_box(examples_text)
                    click.echo(examples_box)

                if anki_card.semantic_component:
                    click.echo(f"    {click.style('Components:', fg='magenta', bold=True)}")
                    component_box = format_meaning_box(anki_card.semantic_component)
                    click.echo(component_box)

                click.echo()

            # Save results if not in dry-run mode
            if not dry_run:
                # Convert to DataFrame and save as CSV
                df_data = []
                for card in anki_cards:
                    df_data.append(
                        {
                            "simplified": card.simplified,
                            "pinyin": card.pinyin,
                            "pronunciation": card.pronunciation,
                            "meaning": card.meaning,
                            "examples": "; ".join(card.examples) if card.examples else None,
                            "phonetic_component": card.phonetic_component,
                            "semantic_component": card.semantic_component,
                            "similar_characters": (
                                "; ".join(card.similar_characters) if card.similar_characters else None
                            ),
                            "passive": card.passive,
                            "alternate_pronunciations": (
                                "; ".join(card.alternate_pronunciations) if card.alternate_pronunciations else None
                            ),
                            "nohearing": card.nohearing,
                        }
                    )

                df = pd.DataFrame(df_data)
                df.to_csv("processed.csv", index=False, header=False)

                # Display summary
                audio_count = sum(1 for card in anki_cards if card.pronunciation)
                click.echo(
                    click.style(f"Converted {len(anki_cards)} cards saved to processed.csv", fg="green", bold=True)
                )
                if audio_count > 0:
                    click.echo(click.style(f"Generated audio for {audio_count}/{len(anki_cards)} cards", fg="green"))
                
                # Report skipped words
                if audio_generator:
                    skipped_words = audio_generator.get_skipped_words()
                    if skipped_words:
                        click.echo()
                        click.echo(click.style(f"Words with no pronunciation selected ({len(skipped_words)}):", fg="yellow", bold=True))
                        for word in skipped_words:
                            click.echo(f"  • {word}")
                        click.echo()
            else:
                audio_count = sum(1 for card in anki_cards if card.pronunciation)
                click.echo(click.style(f"Dry run: Would convert {len(anki_cards)} cards", fg="blue", bold=True))
                if audio and audio_generator:
                    providers_text = ', '.join(audio_generator.get_available_providers())
                    click.echo(click.style(f"Dry run: Would generate audio for cards using providers: {providers_text}", fg="blue"))
                    if audio_dest_dir:
                        click.echo(click.style(f"Dry run: Would copy audio files to: {audio_dest_dir}", fg="blue"))
                    
                    # Report skipped words even in dry-run
                    skipped_words = audio_generator.get_skipped_words()
                    if skipped_words:
                        click.echo()
                        click.echo(click.style(f"Words with no pronunciation selected ({len(skipped_words)}):", fg="yellow", bold=True))
                        for word in skipped_words:
                            click.echo(f"  • {word}")
                        click.echo()

        except Exception as e:
            click.echo(f"Error parsing file: {e}", err=True)
            if verbose:
                import traceback

                traceback.print_exc()
            raise click.Abort()
    else:
        click.echo("Anki Pleco Importer")
        click.echo("Usage: anki-pleco-importer <tsv_file>")
        click.echo("\nOptions:")
        click.echo("  --audio                 Generate pronunciation audio files")
        click.echo("  --audio-providers TEXT  Audio provider (default: forvo)")
        click.echo("  --audio-config PATH     Audio configuration JSON file (default: audio-config.json)")
        click.echo("  --audio-cache-dir PATH  Audio cache directory (default: audio_cache)")
        click.echo("  --audio-dest-dir PATH   Directory to copy selected audio files to")
        click.echo("  --dry-run              Show what would be done without making changes")
        click.echo("  --verbose, -v          Enable verbose output")
        click.echo("\nEnvironment variables:")
        click.echo("  FORVO_API_KEY          Forvo API key")


if __name__ == "__main__":
    main()
