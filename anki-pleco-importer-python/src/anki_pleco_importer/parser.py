import pandas as pd
from pathlib import Path
from typing import Union

from .pleco import PlecoEntry, PlecoCollection


class PlecoTSVParser:
    """Parser for Pleco TSV export files."""

    def parse_file(self, file_path: Union[str, Path]) -> PlecoCollection:
        """Parse a TSV file and return a PlecoCollection."""
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(file_path, sep="\t", header=None, names=["chinese", "pinyin", "definition"])

        entries = []
        for _, row in df.iterrows():
            entry = PlecoEntry(chinese=row["chinese"], pinyin=row["pinyin"], definition=row["definition"])
            entries.append(entry)

        return PlecoCollection(entries=entries)

    def parse_string(self, content: str) -> PlecoCollection:
        """Parse TSV content from a string and return a PlecoCollection."""
        from io import StringIO

        df = pd.read_csv(StringIO(content), sep="\t", header=None, names=["chinese", "pinyin", "definition"])

        entries = []
        for _, row in df.iterrows():
            entry = PlecoEntry(chinese=row["chinese"], pinyin=row["pinyin"], definition=row["definition"])
            entries.append(entry)

        return PlecoCollection(entries=entries)
