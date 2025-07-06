from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel


@dataclass
class PlecoEntry:
    """Represents a single Pleco flashcard entry."""
    chinese: str
    pinyin: str
    definition: str
    
    def __str__(self) -> str:
        return f"{self.chinese} ({self.pinyin}): {self.definition}"


@dataclass
class PlecoCollection:
    """Represents a collection of Pleco flashcard entries."""
    entries: List[PlecoEntry]
    
    def __len__(self) -> int:
        return len(self.entries)
    
    def __iter__(self):
        return iter(self.entries)
    
    def add_entry(self, entry: PlecoEntry) -> None:
        """Add a new entry to the collection."""
        self.entries.append(entry)


class AnkiCard(BaseModel):
    """Represents an Anki flashcard with Chinese learning fields."""
    pinyin: str
    simplified: str
    pronunciation: Optional[str] = None
    meaning: str
    examples: Optional[List[str]] = None
    phonetic_component: Optional[str] = None
    semantic_component: Optional[str] = None
    similar_characters: Optional[List[str]] = None
    passive: bool = False
    alternate_pronunciations: Optional[List[str]] = None
    nohearing: bool = False