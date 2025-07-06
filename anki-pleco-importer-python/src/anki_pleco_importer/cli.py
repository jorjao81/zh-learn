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
            click.echo(click.style(f"Parsed {len(collection)} entries from {tsv_file}:", fg="green", bold=True))
            click.echo()
            
            for i, entry in enumerate(collection, 1):
                click.echo(click.style(f"{i:2d}. {entry.chinese}", fg="cyan", bold=True))
                click.echo(f"    {click.style('Pinyin:', fg='yellow', bold=True)} {entry.pinyin}")
                click.echo(f"    {click.style('Definition:', fg='yellow', bold=True)} {entry.definition}")
                click.echo()
                
        except Exception as e:
            click.echo(f"Error parsing file: {e}", err=True)
            raise click.Abort()
    else:
        click.echo("Anki Pleco Importer")
        click.echo("Usage: anki-pleco-importer <tsv_file>")


if __name__ == "__main__":
    main()
