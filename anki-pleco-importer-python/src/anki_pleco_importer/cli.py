"""Command line interface for Anki Pleco Importer."""

import click
import re
import pandas as pd
import os
import json
import shutil
import random
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from .parser import PlecoTSVParser
from .pleco import pleco_to_anki
from .audio import MultiProviderAudioGenerator
from .anki_parser import AnkiExportParser
from .hsk import HSKWordLists
from .epub_analyzer import ChineseEPUBAnalyzer


def convert_to_html_format(text: str) -> str:
    """Convert text with newlines to HTML format using <br> tags."""
    if not text:
        return text
    return text.replace("\n", "<br>")


def convert_list_to_html_format(items: List[str]) -> str:
    """Convert a list of strings to HTML format with <br> separators."""
    if not items:
        return ""
    return "<br>".join(items)


def format_html_for_terminal(text: str) -> str:
    """Convert simple HTML tags to click formatting for terminal output."""

    # Replace <b>...</b> with click's bold formatting
    def replace_bold(match: re.Match[str]) -> str:
        content = match.group(1)
        return click.style(content, bold=True)

    # Replace <span style="color: red;">...</span> with click's red color formatting
    def replace_red_span(match: re.Match[str]) -> str:
        content = match.group(1)
        return click.style(content, fg="red")

    # Handle bold tags (case insensitive)
    formatted = re.sub(r"<b>(.*?)</b>", replace_bold, text, flags=re.IGNORECASE)

    # Also handle self-closing bold tags if any
    formatted = re.sub(r"<B>(.*?)</B>", replace_bold, formatted)

    # Handle red span tags (case insensitive)
    formatted = re.sub(
        r'<span\s+style="color:\s*red;">(.*?)</span>',
        replace_red_span,
        formatted,
        flags=re.IGNORECASE,
    )

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
        # Try default config files in current directory
        for default_config in ["audio-config.json", "audio_config.json"]:
            if os.path.exists(default_config):
                config_file = default_config
                break

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


@click.group()
@click.version_option()
def cli() -> None:
    """Convert Pleco flashcard exports to Anki-compatible format."""
    pass


@cli.command()
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
@click.option(
    "--audio-dest-dir",
    type=click.Path(),
    help="Directory to copy selected audio files to",
)
@click.option("--dry-run", is_flag=True, help="Show what would be done without making changes")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def convert(
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
                    click.echo(
                        click.style(
                            f"Audio providers available: {', '.join(available_providers)}",
                            fg="green",
                        )
                    )
                else:
                    click.echo(click.style("Warning: No audio providers available", fg="yellow"))
                    # Keep audio_generator to track skipped words even when no providers available

            except Exception as e:
                click.echo(
                    click.style(
                        f"Warning: Failed to initialize audio generation: {e}",
                        fg="yellow",
                    )
                )
                audio_generator = None

        # Create audio destination directory if specified
        if audio_dest_dir and not dry_run:
            try:
                Path(audio_dest_dir).mkdir(parents=True, exist_ok=True)
                if verbose:
                    click.echo(f"Audio destination directory: {audio_dest_dir}")
            except Exception as e:
                click.echo(
                    click.style(
                        f"Warning: Failed to create audio destination directory: {e}",
                        fg="yellow",
                    )
                )
                audio_dest_dir = None

        try:
            collection = parser.parse_file(tsv_file)
            click.echo(
                click.style(
                    f"Parsed {len(collection)} entries from {tsv_file}:",
                    fg="green",
                    bold=True,
                )
            )
            click.echo()

            anki_cards = []
            parser = AnkiExportParser()
            cards = parser.parse_file("Chinese.txt")
            print(len(cards))

            for i, entry in enumerate(collection, 1):
                anki_card = pleco_to_anki(entry, parser)

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
                                    click.echo(
                                        click.style(
                                            f"    Warning: Failed to copy audio to destination: {copy_error}",
                                            fg="yellow",
                                        )
                                    )
                        elif verbose:
                            click.echo(f"    No audio generated for '{anki_card.simplified}'")

                    except Exception as e:
                        if verbose:
                            click.echo(f"    Audio generation failed for '{anki_card.simplified}': {e}")

                anki_cards.append(anki_card)

                # Display card information
                audio_indicator = " 🔊" if anki_card.pronunciation else ""
                styled_number = click.style(f"{i:2d}. {anki_card.simplified} ", fg="cyan", bold=True)
                click.echo(styled_number + anki_card.pinyin + audio_indicator)

                if verbose and anki_card.pronunciation:
                    click.echo(f"    {click.style('Audio:', fg='blue', bold=True)} {anki_card.pronunciation}")

                click.echo(f"    {click.style('Meaning:', fg='yellow', bold=True)}")
                meaning_box = format_meaning_box(anki_card.meaning)
                click.echo(meaning_box)

                if anki_card.examples:
                    click.echo(f"    {click.style('Examples:', fg='green', bold=True)}")
                    examples_text = "\n".join(anki_card.examples)
                    examples_box = format_meaning_box(examples_text)
                    click.echo(examples_box)

                if anki_card.structural_decomposition:
                    click.echo(f"    {click.style('Components:', fg='magenta', bold=True)}")
                    component_box = format_meaning_box(anki_card.structural_decomposition)
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
                            "meaning": convert_to_html_format(card.meaning),
                            "examples": (convert_list_to_html_format(card.examples) if card.examples else None),
                            "phonetic_component": card.phonetic_component,
                            "structural_decomposition": (
                                convert_to_html_format(card.structural_decomposition)
                                if card.structural_decomposition
                                else None
                            ),
                            "similar_characters": (
                                "<br>".join(card.similar_characters) if card.similar_characters else None
                            ),
                            "passive": card.passive,
                            "alternate_pronunciations": (
                                "<br>".join(card.alternate_pronunciations) if card.alternate_pronunciations else None
                            ),
                            "nohearing": card.nohearing,
                        }
                    )

                df = pd.DataFrame(df_data)
                df.to_csv("processed.csv", index=False, header=False)

                # Display summary
                audio_count = sum(1 for card in anki_cards if card.pronunciation)
                click.echo(
                    click.style(
                        f"Converted {len(anki_cards)} cards saved to processed.csv",
                        fg="green",
                        bold=True,
                    )
                )
                if audio_count > 0:
                    click.echo(
                        click.style(
                            f"Generated audio for {audio_count}/{len(anki_cards)} cards",
                            fg="green",
                        )
                    )

                # Report skipped words
                if audio_generator:
                    skipped_words = audio_generator.get_skipped_words()
                    if skipped_words:
                        click.echo()
                        click.echo(
                            click.style(
                                f"Words with no pronunciation selected ({len(skipped_words)}):",
                                fg="yellow",
                                bold=True,
                            )
                        )
                        for word in skipped_words:
                            click.echo(f"  • {word}")
                        click.echo()
            else:
                audio_count = sum(1 for card in anki_cards if card.pronunciation)
                click.echo(
                    click.style(
                        f"Dry run: Would convert {len(anki_cards)} cards",
                        fg="blue",
                        bold=True,
                    )
                )
                if audio and audio_generator:
                    providers_text = ", ".join(audio_generator.get_available_providers())
                    click.echo(
                        click.style(
                            f"Dry run: Would generate audio for cards using providers: {providers_text}",
                            fg="blue",
                        )
                    )
                    if audio_dest_dir:
                        click.echo(
                            click.style(
                                f"Dry run: Would copy audio files to: {audio_dest_dir}",
                                fg="blue",
                            )
                        )

                    # Report skipped words even in dry-run
                    skipped_words = audio_generator.get_skipped_words()
                    if skipped_words:
                        click.echo()
                        click.echo(
                            click.style(
                                f"Words with no pronunciation selected ({len(skipped_words)}):",
                                fg="yellow",
                                bold=True,
                            )
                        )
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


@cli.command()
@click.argument("anki_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--top-candidates",
    "-n",
    default=20,
    help="Number of top candidate characters to show",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def summary(anki_file: Path, top_candidates: int, verbose: bool) -> None:
    """Generate summary statistics for an Anki export file."""

    try:
        parser = AnkiExportParser()
        cards = parser.parse_file(anki_file)

        click.echo(click.style(f"Anki Export Summary for {anki_file}", fg="green", bold=True))
        click.echo("=" * 50)

        # Basic statistics
        click.echo(f"Total cards: {len(cards)}")

        # Character analysis
        all_chars = parser.get_all_characters()
        click.echo(f"Total unique characters: {len(all_chars)}")

        single_chars = parser.get_single_character_words()
        click.echo(f"Single-character words: {len(single_chars)}")

        multi_words = parser.get_multi_character_words()
        click.echo(f"Multi-character words: {len(multi_words)}")

        component_chars = parser.get_component_characters()
        click.echo(f"Characters mentioned as components: {len(component_chars)}")

        # Character frequency
        if verbose:
            char_freq = parser.get_character_frequency()
            click.echo("\nMost frequent characters:")
            sorted_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)
            for char, count in sorted_chars[:10]:
                click.echo(f"  {char}: {count} times")

        # HSK word coverage analysis
        click.echo(f"\n{click.style('HSK Word Coverage Analysis:', fg='blue', bold=True)}")
        try:
            hsk_word_lists = HSKWordLists(Path("."))

            # Get all words from Anki cards
            anki_words = set()
            for card in cards:
                clean_chars = card.get_clean_characters()
                if clean_chars:
                    anki_words.add(clean_chars)

            # Analyze coverage for each HSK level
            hsk_analyses = hsk_word_lists.analyze_all_levels(anki_words)

            if hsk_analyses:
                click.echo(f"Total words in Anki collection: {len(anki_words)}")
                click.echo("\nHSK Level Coverage:")
                click.echo("-" * 50)

                for analysis in hsk_analyses:
                    level_name = f"HSK {analysis.level}" if analysis.level <= 6 else "HSK 7-9"
                    percentage_color = (
                        "green"
                        if analysis.coverage_percentage >= 80
                        else "yellow"
                        if analysis.coverage_percentage >= 50
                        else "red"
                    )

                    click.echo(
                        f"{level_name:8}: "
                        f"{click.style(f'{analysis.coverage_percentage:5.1f}%', fg=percentage_color)} "
                        f"({len(analysis.present_words):4}/{analysis.total_words:4} words)"
                    )

                # Show cumulative coverage
                click.echo("\nCumulative Coverage:")
                click.echo("-" * 30)
                for level in [3, 6]:  # Show cumulative for HSK 1-3 and HSK 1-6
                    if level <= max(analysis.level for analysis in hsk_analyses):
                        cumulative = hsk_word_lists.get_cumulative_coverage(anki_words, level)
                        percentage_color = (
                            "green"
                            if cumulative.coverage_percentage >= 80
                            else "yellow"
                            if cumulative.coverage_percentage >= 50
                            else "red"
                        )

                        click.echo(
                            f"HSK 1-{level}: "
                            f"{click.style(f'{cumulative.coverage_percentage:5.1f}%', fg=percentage_color)} "
                            f"({len(cumulative.present_words):4}/{cumulative.total_words:4} words)"
                        )

                # Show missing words for lower levels if verbose
                if verbose:
                    click.echo(f"\n{click.style('Missing Words by Level:', fg='red', bold=True)}")
                    for analysis in hsk_analyses[:5]:  # Show HSK 1-5 to see random selection in action
                        if analysis.missing_words:
                            level_name = f"HSK {analysis.level}" if analysis.level <= 6 else "HSK 7-9"
                            click.echo(f"\n{level_name} missing words ({len(analysis.missing_words)}):")

                            # Show up to 20 missing words, randomly selected if more than 20
                            max_words_to_show = 20
                            missing_count = len(analysis.missing_words)

                            if missing_count <= max_words_to_show:
                                missing_to_show = analysis.missing_words
                            else:
                                # Randomly select words when there are more than the limit
                                missing_to_show = random.sample(analysis.missing_words, max_words_to_show)
                                # Sort the selected words for consistent display
                                missing_to_show.sort()

                            for i in range(0, len(missing_to_show), 10):
                                row = missing_to_show[i : i + 10]
                                click.echo(f"  {' '.join(row)}")

                            if missing_count > max_words_to_show:
                                click.echo(
                                    f"  ... and {missing_count - max_words_to_show} more (randomly selected above)"
                                )
            else:
                click.echo(
                    "No HSK word lists found. Place HSK1.txt through HSK6.txt and HSK7-9.txt in the current directory."
                )

        except Exception as e:
            click.echo(f"Warning: Could not analyze HSK coverage: {e}")

        # Candidate characters analysis
        click.echo(f"\n{click.style('Candidate Characters to Learn:', fg='yellow', bold=True)}")
        click.echo("(Characters that appear in many words OR as components, but are not single-character words)")

        candidates = parser.analyze_candidate_characters()

        if candidates:
            click.echo(f"\nTop {min(top_candidates, len(candidates))} candidates:")
            for i, candidate in enumerate(candidates[:top_candidates], 1):
                is_component = candidate.character in component_chars
                component_indicator = " 🔧" if is_component else ""
                click.echo(
                    f"{i:2d}. {candidate.character} ({candidate.pinyin}) - "
                    f"score: {candidate.score}, appears in {candidate.word_count} words"
                    f"{component_indicator}"
                )

                if verbose:
                    # Show some words containing this character
                    words_with_char = [word for word in multi_words if candidate.character in word][:5]
                    if words_with_char:
                        click.echo(f"      Found in: {', '.join(words_with_char)}")
        else:
            click.echo("No candidate characters found.")

        click.echo("\n🔧 = Character is also used as a component in other characters")

    except Exception as e:
        click.echo(f"Error analyzing file: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        raise click.Abort()


@cli.command()
@click.argument("anki_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--count",
    "-c",
    default=20,
    help="Number of missing words to show per level (default: 20)",
)
@click.option(
    "--max-level",
    default=6,
    help="Maximum HSK level to check (default: 6, use 7 for HSK 7-9)",
)
@click.option("--verbose", "-v", is_flag=True, help="Show additional statistics")
def missing_hsk(anki_file: Path, count: int, max_level: int, verbose: bool) -> None:
    """Show missing HSK words by level, starting from the lowest level."""

    try:
        # Load Anki cards
        parser = AnkiExportParser()
        cards = parser.parse_file(anki_file)

        # Get all words from Anki cards
        anki_words = set()
        for card in cards:
            clean_chars = card.get_clean_characters()
            if clean_chars:
                anki_words.add(clean_chars)

        # Load HSK word lists
        hsk_word_lists = HSKWordLists(Path("."))
        available_levels = hsk_word_lists.get_available_levels()

        if not available_levels:
            click.echo(
                "No HSK word lists found. Place HSK1.txt through HSK6.txt and HSK7-9.txt in the current directory."
            )
            return

        click.echo(click.style(f"Missing HSK Words from {anki_file}", fg="red", bold=True))
        click.echo("=" * 60)

        if verbose:
            click.echo(f"Anki collection contains {len(anki_words)} unique words")
            click.echo(f"Showing up to {count} missing words per level (levels 1-{max_level})")
            click.echo()

        total_missing = 0
        total_words = 0

        # Check each level from lowest to highest
        for level in sorted(available_levels):
            if level > max_level:
                continue

            analysis = hsk_word_lists.analyze_coverage(anki_words, level)
            total_missing += len(analysis.missing_words)
            total_words += analysis.total_words

            level_name = f"HSK {level}" if level <= 6 else "HSK 7-9"

            # Color code based on coverage
            coverage_color = (
                "green"
                if analysis.coverage_percentage >= 90
                else "yellow"
                if analysis.coverage_percentage >= 70
                else "red"
            )

            click.echo(
                f"{click.style(level_name, fg='blue', bold=True)}: "
                f"{click.style(f'{analysis.coverage_percentage:.1f}%', fg=coverage_color)} coverage "
                f"({len(analysis.present_words)}/{analysis.total_words} words)"
            )

            if analysis.missing_words:
                missing_count = len(analysis.missing_words)
                words_to_show = min(count, missing_count)

                if missing_count <= count:
                    click.echo(f"Missing {missing_count} words:")
                    missing_words = analysis.missing_words
                else:
                    click.echo(f"Missing {missing_count} words (showing random {words_to_show}):")
                    # Randomly select words when there are more than the limit
                    missing_words = random.sample(analysis.missing_words, words_to_show)
                    # Sort the selected words for consistent display
                    missing_words.sort()

                # Display words in rows of 5 for better readability
                for i in range(0, len(missing_words), 5):
                    row = missing_words[i : i + 5]
                    # Format each word with consistent spacing
                    formatted_row = [f"{word:6}" for word in row]
                    click.echo(f"  {' '.join(formatted_row)}")

                if missing_count > words_to_show:
                    click.echo(
                        click.style(f"  ... and {missing_count - words_to_show} more (not shown)", fg="bright_black")
                    )
            else:
                click.echo(click.style("✓ Complete! No missing words", fg="green"))

            click.echo()

        # Show summary statistics
        click.echo(click.style("Summary", fg="cyan", bold=True))
        click.echo("-" * 20)
        overall_coverage = ((total_words - total_missing) / total_words * 100) if total_words > 0 else 0
        summary_color = "green" if overall_coverage >= 80 else "yellow" if overall_coverage >= 60 else "red"

        click.echo(
            f"Overall coverage (HSK 1-{max_level}): "
            f"{click.style(f'{overall_coverage:.1f}%', fg=summary_color)} "
            f"({total_words - total_missing}/{total_words} words)"
        )
        click.echo(
            f"Total missing words: {click.style(str(total_missing), fg='red' if total_missing > 0 else 'green')}"
        )

        if total_missing > 0:
            click.echo()
            click.echo(click.style("💡 Tip:", fg="yellow", bold=True))
            click.echo("Focus on completing lower HSK levels first for maximum learning efficiency!")

    except Exception as e:
        click.echo(f"Error analyzing HSK coverage: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        raise click.Abort()


@cli.command()
@click.argument("epub_file", type=click.Path(exists=True, path_type=Path))
@click.argument("anki_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--target-coverage",
    multiple=True,
    type=int,
    default=[80, 90, 95],
    help="Target coverage percentages to calculate (default: 80, 90, 95)",
)
@click.option(
    "--top-unknown",
    default=50,
    help="Number of top unknown high-frequency words to show (default: 50)",
)
@click.option(
    "--min-frequency",
    default=3,
    help="Minimum word frequency threshold for analysis (default: 3)",
)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed analysis")
def analyze_epub(
    epub_file: Path,
    anki_file: Path,
    target_coverage: Tuple[int, ...],
    top_unknown: int,
    min_frequency: int,
    verbose: bool,
) -> None:
    """Analyze Chinese vocabulary in an EPUB file against your Anki collection."""

    try:
        # Load Anki collection
        click.echo("Loading Anki collection...")
        anki_parser = AnkiExportParser()
        cards = anki_parser.parse_file(anki_file)

        # Get all words from Anki cards
        anki_words = set()
        for card in cards:
            clean_chars = card.get_clean_characters()
            if clean_chars:
                anki_words.add(clean_chars)

        click.echo(f"Loaded {len(anki_words)} words from Anki collection")

        # Initialize EPUB analyzer
        click.echo("Initializing EPUB analyzer...")
        try:
            hsk_word_lists = HSKWordLists(Path("."))
            analyzer = ChineseEPUBAnalyzer(hsk_word_lists)
        except ImportError as e:
            click.echo(f"Error: {e}")
            click.echo("Please install required dependencies:")
            click.echo("  pip install ebooklib jieba")
            raise click.Abort()

        # Analyze EPUB
        click.echo(f"Analyzing EPUB file: {epub_file}")
        analysis = analyzer.analyze_epub(
            epub_file,
            anki_words,
            min_frequency=min_frequency,
            target_coverages=list(target_coverage),
            top_unknown_count=top_unknown,
        )

        # Generate comprehensive report
        _generate_epub_analysis_report(analysis, verbose)

    except Exception as e:
        click.echo(f"Error analyzing EPUB: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        raise click.Abort()


def _generate_epub_analysis_report(analysis, verbose: bool) -> None:
    """Generate and display comprehensive EPUB analysis report."""

    # Header
    click.echo()
    click.echo(click.style("=" * 80, fg="cyan"))
    click.echo(click.style(f"EPUB Vocabulary Analysis: {analysis.title}", fg="cyan", bold=True))
    click.echo(click.style("=" * 80, fg="cyan"))

    # Basic Statistics
    click.echo(f"\n{click.style('📚 Basic Statistics', fg='blue', bold=True)}")
    click.echo("-" * 40)
    click.echo(f"Total words in text: {analysis.stats.total_words:,}")
    click.echo(f"Unique words: {analysis.stats.unique_words:,}")
    click.echo(f"Chinese words: {analysis.stats.chinese_words:,}")
    click.echo(f"Unique Chinese words: {analysis.stats.unique_chinese_words:,}")

    # Vocabulary diversity
    if analysis.stats.total_words > 0:
        diversity = analysis.stats.unique_words / analysis.stats.total_words
        click.echo(f"Vocabulary diversity: {diversity:.3f}")

    # HSK Level Distribution
    click.echo(f"\n{click.style('📊 HSK Level Distribution', fg='green', bold=True)}")
    click.echo("-" * 60)
    click.echo(f"{'Level':8} {'Words':>8} {'Unique':>8} {'% of Text':>10} {'% Unique':>10}")
    click.echo("-" * 60)

    total_classified = 0
    for dist in analysis.hsk_distribution:
        level_name = f"HSK {dist.level}" if dist.level <= 6 else "HSK 7-9"
        click.echo(
            f"{level_name:8} {dist.word_count:>8,} {dist.unique_count:>8} "
            f"{dist.percentage:>9.1f}% {dist.coverage_percentage:>9.1f}%"
        )
        total_classified += dist.word_count

    # Words not in HSK
    unclassified = analysis.stats.total_words - total_classified
    unclassified_pct = (unclassified / analysis.stats.total_words * 100) if analysis.stats.total_words > 0 else 0
    click.echo("-" * 60)
    click.echo(f"{'Non-HSK':8} {unclassified:>8,} {'':>8} {unclassified_pct:>9.1f}% {'':>10}")

    # Known vs Unknown Words
    click.echo(f"\n{click.style('🎯 Vocabulary Knowledge (Anki Collection)', fg='yellow', bold=True)}")
    click.echo("-" * 50)

    known_count = len(analysis.known_words)
    unknown_count = len(analysis.unknown_words)
    total_unique = known_count + unknown_count

    if total_unique > 0:
        known_pct = known_count / total_unique * 100
        unknown_pct = unknown_count / total_unique * 100

        click.echo(f"Known words: {known_count:,} ({known_pct:.1f}%)")
        click.echo(f"Unknown words: {unknown_count:,} ({unknown_pct:.1f}%)")

        # Calculate text coverage by known words
        known_word_freq = sum(freq for word, freq in analysis.word_frequencies.items() if word in analysis.known_words)
        known_coverage = (known_word_freq / analysis.stats.total_words * 100) if analysis.stats.total_words > 0 else 0

        coverage_color = "green" if known_coverage >= 80 else "yellow" if known_coverage >= 60 else "red"
        click.echo(f"Text coverage by known words: {click.style(f'{known_coverage:.1f}%', fg=coverage_color)}")

    # Coverage Targets
    click.echo(f"\n{click.style('🎯 Coverage Targets', fg='magenta', bold=True)}")
    click.echo("-" * 60)
    click.echo(f"{'Target':>8} {'Current':>10} {'Words Needed':>15} {'Priority Words':>15}")
    click.echo("-" * 60)

    for target_pct, target in analysis.coverage_targets.items():
        color = "green" if target.current_coverage >= target_pct else "yellow" if target.words_needed <= 100 else "red"
        click.echo(
            f"{target_pct:>7}% {target.current_coverage:>9.1f}% "
            f"{target.words_needed:>14,} {len(target.priority_words):>14}"
        )

    # High-Frequency Unknown Words
    if analysis.high_frequency_unknown:
        click.echo(f"\n{click.style('🔥 High-Frequency Unknown Words', fg='red', bold=True)}")
        click.echo(f"(Top {len(analysis.high_frequency_unknown)} most frequent unknown words)")
        click.echo("-" * 70)

        # Display in rows of 5 for better readability
        for i in range(0, len(analysis.high_frequency_unknown), 5):
            row = analysis.high_frequency_unknown[i : i + 5]
            formatted_row = [f"{word}({freq})" for word, freq in row]
            click.echo(f"  {' '.join(f'{item:12}' for item in formatted_row)}")

    # Detailed Priority Learning Lists (verbose mode)
    if verbose and analysis.coverage_targets:
        click.echo(f"\n{click.style('📖 Priority Learning Lists (Verbose)', fg='cyan', bold=True)}")

        for target_pct in sorted(analysis.coverage_targets.keys()):
            target = analysis.coverage_targets[target_pct]
            if target.priority_words:
                click.echo(f"\n{click.style(f'For {target_pct}% coverage:', fg='cyan', bold=True)}")
                click.echo(f"Learn these {len(target.priority_words)} words:")

                # Show words in rows of 8 for compact display
                for i in range(0, len(target.priority_words), 8):
                    row = target.priority_words[i : i + 8]
                    formatted_row = [f"{word}({freq})" for word, freq in row]
                    click.echo(f"  {' '.join(f'{item:10}' for item in formatted_row)}")

    # Learning Recommendations
    click.echo(f"\n{click.style('💡 Learning Recommendations', fg='yellow', bold=True)}")
    click.echo("-" * 40)

    if analysis.coverage_targets.get(80):
        target_80 = analysis.coverage_targets[80]
        if target_80.words_needed <= 50:
            click.echo("✅ This book is within reach! Focus on the high-frequency words above.")
        elif target_80.words_needed <= 200:
            click.echo("📚 Moderate difficulty. Consider studying HSK vocabulary first.")
        else:
            click.echo("🚨 High difficulty. Build vocabulary with easier texts first.")

    if analysis.high_frequency_unknown:
        most_frequent = analysis.high_frequency_unknown[0]
        click.echo(f"🎯 Start with '{most_frequent[0]}' (appears {most_frequent[1]} times)")

    # Overall assessment
    avg_hsk_level = _calculate_average_hsk_level(analysis.hsk_distribution)
    if avg_hsk_level:
        if avg_hsk_level <= 3:
            click.echo("📊 Overall difficulty: Beginner (HSK 1-3 level)")
        elif avg_hsk_level <= 5:
            click.echo("📊 Overall difficulty: Intermediate (HSK 4-5 level)")
        else:
            click.echo("📊 Overall difficulty: Advanced (HSK 6+ level)")

    click.echo()


def _calculate_average_hsk_level(hsk_distribution: List) -> Optional[float]:
    """Calculate weighted average HSK level."""
    total_weight = 0
    total_value = 0

    for dist in hsk_distribution:
        if dist.word_count > 0:
            level = min(dist.level, 6)  # Cap at level 6 for calculation
            total_weight += dist.word_count
            total_value += level * dist.word_count

    return total_value / total_weight if total_weight > 0 else None


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
