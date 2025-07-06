"""Command line interface for Anki Pleco Importer."""

import click
from pathlib import Path

from .parser import PlecoTSVParser


@click.command()
@click.argument("tsv_file", type=click.Path(exists=True, path_type=Path), required=False)
@click.version_option()
def main(tsv_file: Path) -> None:
    """Convert Pleco flashcard exports to Anki-compatible format."""
    if tsv_file:
        parser = PlecoTSVParser()
        try:
            collection = parser.parse_file(tsv_file)
            click.echo(f"Parsed {len(collection)} entries from {tsv_file}:\n")
            
            for i, entry in enumerate(collection, 1):
                click.echo(f"{i:2d}. {entry.chinese}")
                click.echo(f"    Pinyin: {entry.pinyin}")
                click.echo(f"    Definition: {entry.definition}")
                click.echo()
                
        except Exception as e:
            click.echo(f"Error parsing file: {e}", err=True)
            raise click.Abort()
    else:
        click.echo("Anki Pleco Importer")
        click.echo("Usage: anki-pleco-importer <tsv_file>")


if __name__ == "__main__":
    main()
