"""
Anki export improver that re-runs structural decomposition for single characters.
Updates component analysis while preserving other fields.
"""

import re
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from .character_decomposer import CharacterDecomposer, ComponentResult
from .anki_parser import AnkiCard

logger = logging.getLogger(__name__)


@dataclass
class ImprovementResult:
    """Result of improving a single card."""

    original_card: AnkiCard
    improved_card: AnkiCard
    changes_made: List[str]
    decomposition_result: Optional[ComponentResult]


class AnkiImprover:
    """Improves Anki exports by re-running structural decomposition for single characters."""

    def __init__(self, update_components: bool = True, update_radicals: bool = True, include_examples: bool = False):
        """Initialize the improver.

        Args:
            update_components: Whether to update the components field
            update_radicals: Whether to update the radicals field
            include_examples: Whether to include reformatted examples in CSV output
        """
        self.update_components = update_components
        self.update_radicals = update_radicals
        self.include_examples = include_examples
        self.decomposer = None

        # Initialize decomposer if needed
        if self.update_components or self.update_radicals:
            try:
                self.decomposer = CharacterDecomposer()
                logger.info("Character decomposer initialized")
            except ImportError as e:
                logger.error(f"Failed to initialize character decomposer: {e}")
                raise

    def improve_file(self, input_file: Path, output_file: Optional[Path] = None) -> List[ImprovementResult]:
        """Improve an Anki export file by creating a new CSV with structural decomposition.

        Args:
            input_file: Path to the input Anki export file
            output_file: Path for the output file (if None, will use input_file with .csv suffix)

        Returns:
            List of improvement results for each processed card
        """
        if output_file is None:
            output_file = input_file.with_suffix(".csv")

        logger.info(f"Creating improved decomposition CSV: {input_file} -> {output_file}")

        # Create simple CSV output
        results = self._create_decomposition_csv(input_file, output_file)

        # Report summary
        changed_count = len(
            [r for r in results if r.changes_made and not any("Error:" in change for change in r.changes_made)]
        )
        error_count = len([r for r in results if any("Error:" in change for change in r.changes_made)])

        logger.info(f"CSV creation complete: {changed_count} characters processed, {error_count} errors")
        logger.info(f"Output written to: {output_file}")

        return results

    def _create_decomposition_csv(self, input_file: Path, output_file: Path) -> List[ImprovementResult]:
        """Create a simple CSV with characters and their structural decomposition."""
        results = []

        # Read the entire file to find single characters
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all single character lines with their pinyin and examples
        lines = content.split("\n")
        single_chars = []

        for line in lines:
            if line.startswith("Chinese"):
                try:
                    parts = line.split("\t")
                    if len(parts) >= 3:
                        # Extract character from field 2
                        characters_field = parts[2]
                        clean_chars = re.sub(r"<[^>]+>", "", characters_field).strip()

                        # Extract pinyin from field 1
                        pinyin_field = parts[1] if len(parts) > 1 else ""

                        # Extract examples from field 4 (definitions) if including examples
                        examples_field = ""
                        if self.include_examples and len(parts) > 4:
                            examples_field = self._reformat_examples(parts[4])

                        # Only process single characters
                        if len(clean_chars) == 1 and self._is_chinese_character(clean_chars):
                            single_chars.append((clean_chars, pinyin_field, examples_field))
                except Exception as e:
                    logger.debug(f"Failed to parse line: {e}")

        logger.info(f"Found {len(single_chars)} single characters to process")

        # Create CSV data
        csv_rows = []

        for char_data in single_chars:
            if self.include_examples:
                character, pinyin, examples = char_data
            else:
                character, pinyin = char_data[0], char_data[1]
                examples = ""

            try:
                if self.decomposer:
                    decomposition_result = self.decomposer.decompose(character)
                    structural_decomposition = self.decomposer.format_decomposition_semantic(decomposition_result)

                    # Create CSV row: Chinese, Pinyin, Structural Decomposition, [Examples]
                    if self.include_examples:
                        csv_rows.append([character, pinyin, structural_decomposition, examples])
                    else:
                        csv_rows.append([character, pinyin, structural_decomposition])

                    # Create result object
                    original_card = AnkiCard(
                        notetype="Chinese",
                        pinyin=pinyin,
                        characters=character,
                        audio="",
                        definitions="",
                        radicals="",
                        components="",
                        tags="",
                    )

                    improved_card = AnkiCard(
                        notetype="Chinese",
                        pinyin=pinyin,
                        characters=character,
                        audio="",
                        definitions="",
                        radicals="",
                        components=structural_decomposition,
                        tags="",
                    )

                    results.append(
                        ImprovementResult(
                            original_card=original_card,
                            improved_card=improved_card,
                            changes_made=["Updated structural decomposition"],
                            decomposition_result=decomposition_result,
                        )
                    )

                    logger.debug(f"Processed {character} ({pinyin}): structural decomposition created")

            except Exception as e:
                logger.error(f"Failed to process character '{character}': {e}")
                results.append(
                    ImprovementResult(
                        original_card=AnkiCard(
                            notetype="Chinese",
                            pinyin=pinyin,
                            characters=character,
                            audio="",
                            definitions="",
                            radicals="",
                            components="",
                            tags="",
                        ),
                        improved_card=AnkiCard(
                            notetype="Chinese",
                            pinyin=pinyin,
                            characters=character,
                            audio="",
                            definitions="",
                            radicals="",
                            components="",
                            tags="",
                        ),
                        changes_made=[f"Error: {e}"],
                        decomposition_result=None,
                    )
                )

        # Write CSV file
        import csv

        with open(output_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            # Write header
            if self.include_examples:
                writer.writerow(["Chinese", "Pinyin", "Structural Decomposition", "Examples"])
            else:
                writer.writerow(["Chinese", "Pinyin", "Structural Decomposition"])
            # Write data
            writer.writerows(csv_rows)

        return results

    def _improve_file_raw(self, input_file: Path, output_file: Path) -> List[ImprovementResult]:
        """Improve file using raw text processing to preserve exact format."""
        results = []

        # Read the entire file
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")
        output_lines = []

        for line in lines:
            if line.startswith("#") or not line.strip():
                # Header or empty line - copy as-is
                output_lines.append(line)
                continue

            # Check if this line starts with a note type (indicates start of a card)
            if line.startswith("Chinese"):
                try:
                    improved_line, result = self._improve_line(line)
                    output_lines.append(improved_line)
                    if result:
                        results.append(result)
                except Exception as e:
                    logger.error(f"Failed to improve line: {e}")
                    output_lines.append(line)  # Keep original on error
            else:
                # Continuation line or non-card line - copy as-is
                output_lines.append(line)

        # Write output
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))

        return results

    def _improve_line(self, line: str) -> Tuple[str, Optional[ImprovementResult]]:
        """Improve a single line and return improved line and result."""
        parts = line.split("\t")

        if len(parts) < 3:
            return line, None

        # Extract character from field 2 (characters field)
        characters_field = parts[2]
        clean_chars = re.sub(r"<[^>]+>", "", characters_field).strip()

        # Only process single characters
        if len(clean_chars) != 1 or not self._is_chinese_character(clean_chars):
            return line, None

        character = clean_chars
        changes_made = []
        decomposition_result = None

        # Create a mock AnkiCard for the result
        original_card = AnkiCard(
            notetype=parts[0],
            pinyin=parts[1],
            characters=parts[2],
            audio=parts[3] if len(parts) > 3 else "",
            definitions=parts[4] if len(parts) > 4 else "",
            radicals=parts[5] if len(parts) > 5 else "",
            components=parts[6] if len(parts) > 6 else "",
            tags="",
        )

        improved_parts = parts.copy()

        # Decompose the character
        if self.decomposer:
            try:
                decomposition_result = self.decomposer.decompose(character)

                # Update radicals field (position 5) if requested
                if self.update_radicals and decomposition_result.components and len(improved_parts) > 5:
                    radical_info = []
                    for i, component in enumerate(decomposition_result.components):
                        meaning = (
                            decomposition_result.radical_meanings[i]
                            if i < len(decomposition_result.radical_meanings)
                            else ""
                        )
                        if meaning:
                            radical_info.append(f"{component} ({meaning})")
                        else:
                            radical_info.append(component)

                    new_radicals = " + ".join(radical_info)
                    if new_radicals != improved_parts[5]:
                        improved_parts[5] = new_radicals
                        changes_made.append("Updated radicals")

                # Update components field (position 6) if requested
                if self.update_components and len(improved_parts) > 6:
                    new_components = self.decomposer.format_decomposition_semantic(decomposition_result)
                    if new_components != improved_parts[6]:
                        improved_parts[6] = new_components
                        changes_made.append("Updated components")

            except Exception as e:
                logger.warning(f"Failed to decompose character '{character}': {e}")
                changes_made.append(f"Decomposition error: {e}")

        # Create improved card
        improved_card = AnkiCard(
            notetype=improved_parts[0],
            pinyin=improved_parts[1],
            characters=improved_parts[2],
            audio=improved_parts[3] if len(improved_parts) > 3 else "",
            definitions=improved_parts[4] if len(improved_parts) > 4 else "",
            radicals=improved_parts[5] if len(improved_parts) > 5 else "",
            components=improved_parts[6] if len(improved_parts) > 6 else "",
            tags="",
        )

        result = ImprovementResult(
            original_card=original_card,
            improved_card=improved_card,
            changes_made=changes_made,
            decomposition_result=decomposition_result,
        )

        improved_line = "\t".join(improved_parts)
        return improved_line, result

    def _parse_anki_export(self, file_path: Path) -> List[AnkiCard]:
        """Parse an Anki export file into AnkiCard objects."""
        cards = []
        separator = "\t"
        html_mode = False

        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                # Handle header lines
                if line.startswith("#"):
                    if line.startswith("#separator:"):
                        sep_name = line.split(":")[1]
                        if sep_name == "tab":
                            separator = "\t"
                        elif sep_name == "comma":
                            separator = ","
                    elif line.startswith("#html:"):
                        html_mode = line.split(":")[1].lower() == "true"
                    continue

                # Parse card data
                parts = line.split(separator)
                if len(parts) >= 5:  # Minimum required fields
                    try:
                        # Store original parts for exact reconstruction
                        card = AnkiCard(
                            notetype=parts[0] if len(parts) > 0 else "",
                            pinyin=parts[1] if len(parts) > 1 else "",
                            characters=parts[2] if len(parts) > 2 else "",
                            audio=parts[3] if len(parts) > 3 else "",
                            definitions=parts[4] if len(parts) > 4 else "",
                            components=parts[6] if len(parts) > 6 else "",  # Field 6 in this format
                            radicals=parts[5] if len(parts) > 5 else "",  # Field 5 in this format
                            tags="",  # Not used in this format
                        )
                        # Store original parts for reconstruction
                        card._original_parts = parts
                        cards.append(card)
                    except Exception as e:
                        logger.warning(f"Failed to parse line {line_num}: {e}")

        return cards

    def _filter_single_characters(self, cards: List[AnkiCard]) -> List[AnkiCard]:
        """Filter cards that contain single Chinese characters."""
        single_char_cards = []

        for card in cards:
            clean_chars = card.get_clean_characters()
            if len(clean_chars) == 1 and self._is_chinese_character(clean_chars):
                single_char_cards.append(card)

        return single_char_cards

    def _is_chinese_character(self, char: str) -> bool:
        """Check if a character is a Chinese character."""
        return "\u4e00" <= char <= "\u9fff"

    def _reformat_examples(self, examples_text: str) -> str:
        """Reformat examples text with cleaner styling.

        Args:
            examples_text: Raw examples text from Anki export

        Returns:
            Reformatted examples with improved styling
        """
        if not examples_text.strip():
            return examples_text

        # Clean up HTML entities and tags
        formatted = examples_text

        # Replace HTML entities
        formatted = formatted.replace("&nbsp;", " ")
        formatted = formatted.replace("&amp;", "&")
        formatted = formatted.replace("&lt;", "<")
        formatted = formatted.replace("&gt;", ">")
        formatted = formatted.replace("⟾&nbsp;", "⟾ ")
        formatted = formatted.replace("⇒&nbsp;", "⇒ ")

        # Clean up excessive spaces (3+ spaces become 2 spaces for readability)
        formatted = re.sub(r" {3,}", "  ", formatted)

        # Replace bold tags with semantic span styling
        formatted = re.sub(r"<b>(.*?)</b>", r'<span class="example-header">\1</span>', formatted)

        # Format example entries (word + pinyin + definition pattern)
        # Pattern like: 屏息   bǐng xī   hold one's breath
        formatted = re.sub(
            r"(\S+)\s+([a-zA-Züáéíóúàèìòùāēīōūǎěǐǒǔäöü\s]+)\s+([^<\n]+)",
            r'<div class="word-example"><span class="word">\1</span> <span class="pinyin">\2</span> <span class="definition">\3</span></div>',
            formatted,
        )

        # Clean up line breaks
        formatted = formatted.replace("<br><br>", "<br/>")
        formatted = formatted.replace("<br>", "<br/>")

        # Wrap in container if it has structured content
        if any(
            marker in formatted for marker in ['<span class="example-header">', '<div class="word-example">', "⇒", "⟾"]
        ):
            formatted = f'<div class="examples-container">{formatted}</div>'

        return formatted

    def _improve_card(self, card: AnkiCard) -> ImprovementResult:
        """Improve a single card by updating its structural decomposition."""
        character = card.get_clean_characters()
        changes_made = []
        decomposition_result = None

        # Create a copy of the card to modify
        improved_card = AnkiCard(
            notetype=card.notetype,
            pinyin=card.pinyin,
            characters=card.characters,
            audio=card.audio,
            definitions=card.definitions,
            components=card.components,
            radicals=card.radicals,
            tags=card.tags,
        )

        # Only decompose if we have a decomposer and single character
        if self.decomposer and len(character) == 1:
            try:
                decomposition_result = self.decomposer.decompose(character)

                # Update components field if requested
                if self.update_components:
                    new_components = self.decomposer.format_decomposition_semantic(decomposition_result)
                    if new_components != card.components:
                        improved_card.components = new_components
                        changes_made.append("Updated components")

                # Update radicals field if requested
                if self.update_radicals and decomposition_result.components:
                    # Create a simplified radical representation
                    radical_info = []
                    for i, component in enumerate(decomposition_result.components):
                        meaning = (
                            decomposition_result.radical_meanings[i]
                            if i < len(decomposition_result.radical_meanings)
                            else ""
                        )
                        if meaning:
                            radical_info.append(f"{component} ({meaning})")
                        else:
                            radical_info.append(component)

                    new_radicals = " + ".join(radical_info)
                    if new_radicals != card.radicals:
                        improved_card.radicals = new_radicals
                        changes_made.append("Updated radicals")

            except Exception as e:
                logger.warning(f"Failed to decompose character '{character}': {e}")
                changes_made.append(f"Decomposition error: {e}")

        return ImprovementResult(
            original_card=card,
            improved_card=improved_card,
            changes_made=changes_made,
            decomposition_result=decomposition_result,
        )

    def _merge_improvements(self, all_cards: List[AnkiCard], improvements: List[ImprovementResult]) -> List[AnkiCard]:
        """Merge improvements back into the full card list."""
        # Create a mapping of original cards to improved cards
        improvement_map = {}
        for result in improvements:
            improvement_map[id(result.original_card)] = result.improved_card

        # Replace cards that were improved
        merged_cards = []
        for card in all_cards:
            if id(card) in improvement_map:
                merged_cards.append(improvement_map[id(card)])
            else:
                merged_cards.append(card)

        return merged_cards

    def _write_anki_export(self, cards: List[AnkiCard], output_file: Path, input_file: Path) -> None:
        """Write improved cards back to an Anki export file."""
        # Read the header from the original file
        header_lines = []
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    header_lines.append(line)
                else:
                    break

        # Write the output file
        with open(output_file, "w", encoding="utf-8") as f:
            # Write header
            for header_line in header_lines:
                f.write(header_line + "\n")

            # Write cards using original field structure
            for card in cards:
                if hasattr(card, "_original_parts") and card._original_parts is not None:
                    # Use original parts and only update the fields we changed
                    parts = card._original_parts.copy()

                    # Update only the fields we modified
                    if len(parts) > 5:
                        parts[5] = card.radicals  # Radicals in field 5
                    if len(parts) > 6:
                        parts[6] = card.components  # Components in field 6

                    f.write("\t".join(parts) + "\n")
                else:
                    # Fallback: create minimal field structure
                    fields = [
                        card.notetype,
                        card.pinyin,
                        card.characters,
                        card.audio,
                        card.definitions,
                        card.radicals,
                        card.components,
                    ]
                    f.write("\t".join(fields) + "\n")


def improve_anki_export(
    input_file: str, output_file: Optional[str] = None, update_components: bool = True, update_radicals: bool = True
) -> List[ImprovementResult]:
    """Convenience function to improve an Anki export file.

    Args:
        input_file: Path to input Anki export file
        output_file: Path for output file (optional)
        update_components: Whether to update components field
        update_radicals: Whether to update radicals field

    Returns:
        List of improvement results
    """
    improver = AnkiImprover(update_components=update_components, update_radicals=update_radicals)

    return improver.improve_file(Path(input_file), Path(output_file) if output_file else None)


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Improve Anki export by re-running structural decomposition")
    parser.add_argument("input_file", help="Input Anki export file")
    parser.add_argument("-o", "--output", help="Output file (default: input_file.improved.txt)")
    parser.add_argument("--no-components", action="store_true", help="Don't update components field")
    parser.add_argument("--no-radicals", action="store_true", help="Don't update radicals field")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    # Set up logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    # Run improvement
    try:
        results = improve_anki_export(
            args.input_file, args.output, update_components=not args.no_components, update_radicals=not args.no_radicals
        )

        # Print summary
        changed_count = len(
            [r for r in results if r.changes_made and not any("Error:" in change for change in r.changes_made)]
        )
        error_count = len([r for r in results if any("Error:" in change for change in r.changes_made)])

        print(f"\n✅ Improvement complete!")
        print(f"   📊 {len(results)} single characters processed")
        print(f"   ✏️  {changed_count} cards improved")
        print(f"   ❌ {error_count} errors")

        if args.verbose and changed_count > 0:
            print(f"\n📝 Changed cards:")
            for result in results:
                if result.changes_made and not any("Error:" in change for change in result.changes_made):
                    char = result.improved_card.get_clean_characters()
                    changes = ", ".join(result.changes_made)
                    print(f"   {char}: {changes}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
