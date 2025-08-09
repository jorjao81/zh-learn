"""Anki-related models and functionality."""

from typing import List, Optional
from pydantic import BaseModel


class AnkiCard(BaseModel):
    """Represents an Anki flashcard with Chinese learning fields."""

    pinyin: str
    simplified: str
    pronunciation: Optional[str] = None
    meaning: str
    examples: Optional[List[str]] = None
    phonetic_component: Optional[str] = None
    structural_decomposition: Optional[str] = None
    etymology: Optional[str] = None
    similar_characters: Optional[List[str]] = None
    passive: bool = False
    alternate_pronunciations: Optional[List[str]] = None
    nohearing: bool = False
