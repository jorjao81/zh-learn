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
from .hsk import HSKWordLists
from .epub_analyzer import ChineseEPUBAnalyzer
from .anki_parser import AnkiExportParser, AnkiCard


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

                            # Add pinyin to missing words display
                            try:
                                from pypinyin import lazy_pinyin, Style

                                for i in range(0, len(missing_to_show), 8):
                                    row = missing_to_show[i : i + 8]
                                    formatted_row = []
                                    for word in row:
                                        try:
                                            pinyin = "".join(lazy_pinyin(word, style=Style.TONE))
                                            formatted_row.append(f"{word}[{pinyin}]")
                                        except Exception:
                                            formatted_row.append(word)
                                    click.echo(f"  {' '.join(f'{item:14}' for item in formatted_row)}")
                            except ImportError:
                                # Fallback to original format if pypinyin not available
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

                # Display words with pinyin in rows for better readability
                try:
                    from pypinyin import lazy_pinyin, Style

                    # Show fewer words per row to accommodate pinyin
                    for i in range(0, len(missing_words), 4):
                        row = missing_words[i : i + 4]
                        formatted_row = []
                        for word in row:
                            try:
                                pinyin = "".join(lazy_pinyin(word, style=Style.TONE))
                                formatted_row.append(f"{word}[{pinyin}]")
                            except Exception:
                                formatted_row.append(word)
                        click.echo(f"  {' '.join(f'{item:16}' for item in formatted_row)}")
                except ImportError:
                    # Fallback to original format if pypinyin not available
                    for i in range(0, len(missing_words), 5):
                        row = missing_words[i : i + 5]
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
    default=[80, 90, 95, 98],
    help="Target coverage percentages to calculate (default: 80, 90, 95, 98)",
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
@click.option(
    "--proper-names-file",
    type=click.Path(exists=True, path_type=Path),
    help="File containing proper names to treat as known (one per line)",
)
@click.option(
    "--known-words-file",
    type=click.Path(exists=True, path_type=Path),
    help="File containing additional words to treat as known (one per line)",
)
def analyze_epub(
    epub_file: Path,
    anki_file: Path,
    target_coverage: Tuple[int, ...],
    top_unknown: int,
    min_frequency: int,
    verbose: bool,
    proper_names_file: Optional[Path],
    known_words_file: Optional[Path],
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

        # Load proper names file if provided
        proper_names = set()
        if proper_names_file:
            click.echo(f"Loading proper names from {proper_names_file}...")
            try:
                with open(proper_names_file, "r", encoding="utf-8") as f:
                    proper_names = {line.strip() for line in f if line.strip()}
                click.echo(f"Loaded {len(proper_names)} proper names")
                # Add proper names to known words
                anki_words.update(proper_names)
            except Exception as e:
                click.echo(f"Warning: Failed to load proper names file: {e}")

        # Load additional known words file if provided
        additional_known = set()
        if known_words_file:
            click.echo(f"Loading additional known words from {known_words_file}...")
            try:
                with open(known_words_file, "r", encoding="utf-8") as f:
                    additional_known = {line.strip() for line in f if line.strip()}
                click.echo(f"Loaded {len(additional_known)} additional known words")
                # Add to known words
                anki_words.update(additional_known)
            except Exception as e:
                click.echo(f"Warning: Failed to load additional known words file: {e}")

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
        _generate_epub_analysis_report(analysis, verbose, list(target_coverage))

    except Exception as e:
        click.echo(f"Error analyzing EPUB: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        raise click.Abort()


def _generate_epub_analysis_report(analysis, verbose: bool, target_coverages: List[int]) -> None:
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
    non_hsk_unique = len(analysis.non_hsk_words)
    non_hsk_unique_pct = (non_hsk_unique / analysis.stats.unique_words * 100) if analysis.stats.unique_words > 0 else 0
    click.echo("-" * 60)
    click.echo(
        f"{'Non-HSK':8} {unclassified:>8,} {non_hsk_unique:>8} {unclassified_pct:>9.1f}% {non_hsk_unique_pct:>9.1f}%"
    )

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
    click.echo("-" * 30)
    click.echo(f"{'Target':>8} {'Words Needed':>15}")
    click.echo("-" * 30)

    for target_pct, target in analysis.coverage_targets.items():
        click.echo(f"{target_pct:>7}% {target.words_needed:>14,}")

    # High-Frequency Unknown Words
    if analysis.high_frequency_unknown:
        click.echo(f"\n{click.style('🔥 High-Frequency Unknown Words', fg='red', bold=True)}")
        click.echo(f"(Top {len(analysis.high_frequency_unknown)} most frequent unknown words)")
        click.echo("-" * 80)

        # Table headers
        click.echo(f"{'Word':>6} {'Pinyin':<15} {'Freq':>6} {'HSK Level':<10}")
        click.echo("-" * 80)

        # Display words in a clean table format (show top 20)
        for word, freq, pinyin, hsk_level in analysis.high_frequency_unknown[:20]:
            hsk_text = f"HSK {hsk_level}" if hsk_level else "non-HSK"
            if hsk_level and hsk_level <= 4:
                hsk_color = "green"
            elif hsk_level:
                hsk_color = "yellow"
            else:
                hsk_color = "red"

            # Format without color first to get proper alignment
            formatted_line = f"{word:>6} {pinyin:<15} {freq:>6,} {hsk_text:<10}"
            # Replace the HSK text with colored version
            colored_hsk = click.style(hsk_text, fg=hsk_color)
            formatted_line = formatted_line.replace(hsk_text, colored_hsk)
            click.echo(formatted_line)

        # Show count if truncated
        if len(analysis.high_frequency_unknown) > 20:
            remaining = len(analysis.high_frequency_unknown) - 20
            click.echo(f"\n  ... and {remaining} more words " "(use --verbose for full list)")

    # Detailed Priority Learning Lists (verbose mode)
    if verbose and analysis.coverage_targets:
        # Show only the highest target percentage
        highest_target_pct = max(target_coverages) if target_coverages else 98

        if highest_target_pct in analysis.coverage_targets:
            target = analysis.coverage_targets[highest_target_pct]
            if target.priority_words:
                click.echo(f"\n{click.style('📖 Priority Learning List (Verbose)', fg='cyan', bold=True)}")
                click.echo(f"\n{click.style(f'For {highest_target_pct}% coverage:', fg='cyan', bold=True)}")
                click.echo(f"Learn these {len(target.priority_words)} words:")

                # Limit output to first 50 words for readability in table format
                display_words = target.priority_words[:50]

                # Table headers
                click.echo("-" * 80)
                click.echo(f"{'Word':>6} {'Pinyin':<15} {'Freq':>6} {'HSK Level':<10}")
                click.echo("-" * 80)

                # Display words in clean table format
                for word, freq, pinyin, hsk_level in display_words:
                    hsk_text = f"HSK {hsk_level}" if hsk_level else "non-HSK"
                    if hsk_level and hsk_level <= 4:
                        hsk_color = "green"
                    elif hsk_level:
                        hsk_color = "yellow"
                    else:
                        hsk_color = "red"

                    # Format without color first to get proper alignment
                    formatted_line = f"{word:>6} {pinyin:<15} {freq:>6,} {hsk_text:<10}"
                    # Replace the HSK text with colored version
                    colored_hsk = click.style(hsk_text, fg=hsk_color)
                    formatted_line = formatted_line.replace(hsk_text, colored_hsk)
                    click.echo(formatted_line)

                # Show truncation message if there are more words
                if len(target.priority_words) > 50:
                    remaining = len(target.priority_words) - 50
                    click.echo(f"  ... and {remaining} more words")

    # HSK Learning Targets
    if analysis.hsk_learning_targets:
        click.echo(f"\n{click.style('📚 HSK Learning Targets', fg='blue', bold=True)}")
        click.echo("(Words to learn by HSK level, ordered by frequency in this book)")

        for target in analysis.hsk_learning_targets:
            if target.unknown_words:  # Only show levels with unknown words
                click.echo(f"\n{click.style(f'HSK Level {target.level}:', fg='blue', bold=True)}")
                click.echo(
                    f"  Coverage gain: {target.potential_coverage_gain:.1f}% "
                    f"({target.total_word_count:,} word occurrences)"
                )
                click.echo(f"  Words to learn: {len(target.unknown_words)}")

                # Show top 10 words for each level
                display_words = target.unknown_words[:10]
                click.echo("-" * 60)
                click.echo(f"{'Word':>6} {'Pinyin':<15} {'Freq':>6}")
                click.echo("-" * 60)

                for word, freq, pinyin in display_words:
                    click.echo(f"{word:>6} {pinyin:<15} {freq:>6,}")

                # Show truncation message if there are more words
                if len(target.unknown_words) > 10:
                    remaining = len(target.unknown_words) - 10
                    click.echo(f"\n  ... and {remaining} more HSK {target.level} words")

    click.echo()


@cli.command()
@click.argument("anki_file", type=click.Path(exists=True, path_type=Path))
@click.option("--max-suggestions", default=10, help="Maximum number of improvement suggestions to show (default: 10)")
@click.option("--min-word-length", default=3, help="Minimum word length to analyze (default: 3 characters)")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed analysis including both decompositions")
@click.option("--show-all", is_flag=True, help="Show all analyzed words, even those without improvements")
@click.option(
    "--export-csv",
    type=click.Path(path_type=Path),
    help="Export improved cards to CSV file (default: improved_cards.txt)",
)
def improve_cards(
    anki_file: Path,
    max_suggestions: int,
    min_word_length: int,
    verbose: bool,
    show_all: bool,
    export_csv: Optional[Path],
) -> None:
    """Analyze existing Anki cards and suggest improvements to semantic decompositions.

    This command looks for cards with words of 3+ characters and compares the existing
    semantic decomposition with a new dictionary-based decomposition. If the new
    decomposition has fewer components, it suggests an improvement.
    """
    click.echo(f"🔍 Analyzing Anki cards from: {anki_file}")

    try:
        # Parse Anki export file
        parser = AnkiExportParser()
        cards = parser.parse_file(anki_file)
        click.echo(f"Found {len(cards)} cards to analyze")

        # Build dictionary for decomposition
        anki_dictionary = {}
        for card in cards:
            clean_chars = card.get_clean_characters()
            if clean_chars and len(clean_chars) >= 1:
                anki_dictionary[clean_chars] = {"pinyin": card.pinyin, "definition": card.definitions}

        # Find improvement suggestions
        suggestions = _analyze_card_improvements(cards, anki_dictionary, min_word_length, show_all)

        # Sort by component count difference (biggest improvements first) then randomize within groups
        import random

        suggestions.sort(key=lambda x: x["component_reduction"], reverse=True)

        # Randomize suggestions to show variety instead of always the same top ones
        random.shuffle(suggestions)

        # Display results
        if not suggestions:
            click.echo("✅ No improvement suggestions found!")
            click.echo("All cards appear to have optimal decompositions.")
        else:
            # Limit to max suggestions
            suggestions_to_show = suggestions[:max_suggestions]

            click.echo(f"\n🎯 Found {click.style(str(len(suggestions)), fg='cyan', bold=True)} improvement suggestions")
            if len(suggestions) > max_suggestions:
                click.echo(f"(Showing {max_suggestions} random suggestions)")

            for i, suggestion in enumerate(suggestions_to_show, 1):
                _display_improvement_suggestion(suggestion, i, verbose)
                if i < len(suggestions_to_show):  # Don't show separator after last item
                    click.echo(click.style("─" * 80, fg="blue", dim=True))

            if len(suggestions) > max_suggestions:
                remaining = len(suggestions) - max_suggestions
                click.echo(f"\n💡 {remaining} more suggestions available (use --max-suggestions to see more)")

            # Always export CSV of improved cards
            if not export_csv:
                export_csv = Path("improved_cards.txt")

            exported_count = _export_improved_cards_to_csv(cards, suggestions, export_csv, anki_file)
            if exported_count > 0:
                click.echo(f"\n📄 Exported {exported_count} improved cards to: {export_csv}")
            else:
                click.echo("\n📄 No cards needed improvement - no CSV exported")

    except Exception as e:
        click.echo(f"Error analyzing cards: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        raise click.Abort()


def _analyze_card_improvements(
    cards: List[AnkiCard], anki_dictionary: dict, min_word_length: int, show_all: bool
) -> List[dict]:
    """Analyze cards for potential decomposition improvements."""
    from .chinese import get_structural_decomposition

    suggestions = []

    for card in cards:
        clean_chars = card.get_clean_characters()

        # Skip cards that don't meet criteria
        if not clean_chars or len(clean_chars) < min_word_length:
            continue

        # Get current decomposition component count
        # If no components field, treat as character-by-character (worst case)
        if not card.components or card.components.strip() == "":
            current_components = len(clean_chars)  # Character-by-character count
            current_decomposition_display = f"(no decomposition - {len(clean_chars)} characters)"
        else:
            current_components = _count_decomposition_components(card.components)
            current_decomposition_display = card.components
            if current_components == 0:
                continue

        # Generate new decomposition using dictionary-based approach
        try:
            # Create a modified dictionary that excludes the target word itself to force decomposition
            modified_dictionary = {k: v for k, v in anki_dictionary.items() if k != clean_chars}
            new_decomposition = get_structural_decomposition(clean_chars, modified_dictionary)
            new_components = _count_decomposition_components(new_decomposition)

            # For comparison, also get character-by-character decomposition
            from .chinese import _get_individual_character_definitions

            char_by_char = _get_individual_character_definitions(clean_chars)
            char_by_char_components = _count_decomposition_components(char_by_char)

            # Use the better decomposition (dictionary-based vs character-by-character)
            # If dictionary-based has fewer components and is better than character-by-character, use it
            if new_components > 0 and new_components < char_by_char_components:
                best_decomposition = new_decomposition
                best_component_count = new_components
            else:
                best_decomposition = char_by_char
                best_component_count = char_by_char_components

            # Create analysis record
            analysis = {
                "word": clean_chars,
                "pinyin": card.pinyin,
                "definition": card.definitions,
                "current_decomposition": current_decomposition_display,
                "current_component_count": current_components,
                "suggested_decomposition": best_decomposition,
                "suggested_component_count": best_component_count,
                "component_reduction": current_components - best_component_count,
            }

            # Check if new decomposition has fewer components (better semantic grouping)
            if best_component_count > 0 and best_component_count < current_components:
                suggestions.append(analysis)
            elif show_all and best_component_count > 0:
                # Include all analyzed words if show_all is enabled
                analysis["component_reduction"] = 0  # Mark as no improvement
                suggestions.append(analysis)

        except Exception as e:
            # Skip cards that cause errors in decomposition
            if show_all:
                click.echo(f"Error processing {clean_chars}: {e}", err=True)
            continue

    return suggestions


def _count_decomposition_components(decomposition: str) -> int:
    """Count the number of components in a decomposition string."""
    if not decomposition or decomposition.strip() == "":
        return 0

    # Count by splitting on '+' and filtering out empty parts
    parts = [part.strip() for part in decomposition.split("+") if part.strip()]
    return len(parts)


def _display_improvement_suggestion(suggestion: dict, index: int, verbose: bool) -> None:
    """Display a single improvement suggestion with formatting."""
    word = suggestion["word"]
    pinyin = suggestion["pinyin"]
    definition = suggestion["definition"]
    current_count = suggestion["current_component_count"]
    suggested_count = suggestion["suggested_component_count"]
    reduction = suggestion["component_reduction"]

    # Header with word info
    click.echo(
        f"\n{click.style(f'{index}.', fg='blue', bold=True)} "
        f"{click.style(word, fg='cyan', bold=True)} "
        f"[{click.style(pinyin, fg='yellow')}]"
    )

    # Clean up definition by removing HTML tags and limiting length
    clean_definition = _clean_definition(definition)
    if len(clean_definition) > 80:
        clean_definition = clean_definition[:77] + "..."
    click.echo(f"   {click.style(clean_definition, fg='white', dim=True)}")

    # Component count improvement with better visual indicators
    if reduction > 0:
        reduction_color = "green" if reduction >= 3 else "yellow" if reduction == 2 else "cyan"
        reduction_icon = "🔥" if reduction >= 5 else "✨" if reduction >= 3 else "💡"
        click.echo(
            f"   {reduction_icon} {click.style(f'{current_count} → {suggested_count}', fg='white')} "
            f"({click.style(f'-{reduction}', fg=reduction_color, bold=True)} components)"
        )
    else:
        click.echo(f"   ➡️  {click.style(f'{current_count} → {suggested_count}', fg='white')} (no improvement)")

    # Show decompositions with better formatting
    click.echo()
    if verbose and suggestion["current_decomposition"] != f"(no decomposition - {current_count} characters)":
        current_format = _format_decomposition(suggestion["current_decomposition"])
        click.echo(f"   {click.style('Current:', fg='red', bold=True)}   {current_format}")
    suggested_format = _format_decomposition(suggestion["suggested_decomposition"])
    click.echo(f"   {click.style('Suggested:', fg='green', bold=True)} {suggested_format}")


def _clean_definition(definition: str) -> str:
    """Convert HTML formatting to Click styling and clean up text."""
    return _convert_html_to_click_styling(definition)


def _convert_html_to_click_styling(text: str) -> str:
    """Convert HTML tags to Click styling."""
    import re

    if not text:
        return ""

    # Handle HTML entities
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")

    # Convert common HTML tags to Click styling
    # Bold
    text = re.sub(r"<b>(.*?)</b>", lambda m: click.style(m.group(1), bold=True), text, flags=re.DOTALL)
    text = re.sub(r"<strong>(.*?)</strong>", lambda m: click.style(m.group(1), bold=True), text, flags=re.DOTALL)

    # Color styling - handle various color formats
    text = re.sub(
        r'<span style="color:\s*rgb\((\d+),\s*(\d+),\s*(\d+)\);">(.*?)</span>',
        lambda m: click.style(m.group(4), fg="cyan" if int(m.group(1)) < 100 else "white"),
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r'<span style="[^"]*color[^"]*">(.*?)</span>',
        lambda m: click.style(m.group(1), fg="cyan"),
        text,
        flags=re.DOTALL,
    )

    # Div tags - treat as breaks or emphasis
    text = re.sub(r"<div[^>]*>(.*?)</div>", r" \1 ", text, flags=re.DOTALL)

    # Line breaks
    text = re.sub(r"<br\s*/?>", " ", text)

    # Remove any remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Clean up whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove extra quotes and HTML escaping
    text = text.replace('""', '"').replace('""""', '"').replace("&quot;", '"')

    # Remove leading/trailing quotes if they wrap the whole string
    text = text.strip()
    if text.startswith('"') and text.endswith('"') and text.count('"') == 2:
        text = text[1:-1]

    return text.strip()


def _format_decomposition(decomposition: str) -> str:
    """Format decomposition for better readability."""
    if not decomposition:
        return ""

    # If it's a "no decomposition" message, style it differently
    if decomposition.startswith("(no decomposition"):
        return click.style(decomposition, fg="red", dim=True)

    # Split by + and format each component
    parts = [part.strip() for part in decomposition.split("+") if part.strip()]
    formatted_parts = []

    for part in parts:
        # Convert HTML to styling for the part
        styled_part = _convert_html_to_click_styling(part)

        # Extract Chinese character(s) from the component
        if "(" in styled_part:
            chinese = styled_part.split("(")[0].strip()
            rest = "(" + styled_part.split("(", 1)[1]
            # Limit the definition part to keep it readable
            if len(rest) > 50:
                rest = rest[:47] + "...)"
            formatted_parts.append(
                f"{click.style(chinese, fg='cyan', bold=True)}{click.style(rest, fg='white', dim=True)}"
            )
        else:
            formatted_parts.append(click.style(styled_part, fg="cyan", bold=True))

    return f" {click.style('+', fg='yellow')} ".join(formatted_parts)


def _export_improved_cards_to_csv(
    cards: List[AnkiCard], suggestions: List[dict], export_path: Path, original_file: Path
) -> int:
    """Export cards with improved decompositions to a CSV file."""
    # Create a mapping of words to their improved decompositions
    improvements_map = {}
    for suggestion in suggestions:
        if suggestion["component_reduction"] > 0:  # Only include actual improvements
            improvements_map[suggestion["word"]] = suggestion["suggested_decomposition"]

    if not improvements_map:
        return 0

    # Read the original file to preserve the exact format
    with open(original_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find header lines and determine separator
    separator = "\t"  # default
    header_lines = []
    data_start_index = 0

    for i, line in enumerate(lines):
        if line.startswith("#"):
            header_lines.append(line)
            if line.startswith("#separator:"):
                sep_name = line.split(":")[1].strip()
                if sep_name == "comma":
                    separator = ","
            data_start_index = i + 1
        else:
            break

    # Write the improved cards
    exported_count = 0
    with open(export_path, "w", encoding="utf-8") as f:
        # Write header lines
        for header in header_lines:
            f.write(header)

        # Process each data line
        for line in lines[data_start_index:]:
            line = line.strip()
            if not line:
                continue

            parts = line.split(separator)
            if len(parts) >= 6:  # Must have at least components field
                # Extract the characters field (index 2) and components field (index 5)
                characters_field = parts[2] if len(parts) > 2 else ""

                # Get clean characters for matching
                import re

                clean_chars = re.sub(r"<[^>]+>", "", characters_field).strip()

                # Check if this card has an improvement
                if clean_chars in improvements_map:
                    # Replace the components field (index 5) with the improved decomposition
                    parts[5] = improvements_map[clean_chars]
                    exported_count += 1

                # Write the line (improved or unchanged)
                f.write(separator.join(parts) + "\n")
            else:
                # Write unchanged line if it doesn't have enough fields
                f.write(line + "\n")

    return exported_count


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
