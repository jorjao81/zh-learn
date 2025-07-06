"""Command line interface for Anki Pleco Importer."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Convert Pleco flashcard exports to Anki-compatible format."""
    click.echo("Anki Pleco Importer - Coming soon!")


if __name__ == "__main__":
    main()
