from dataclasses import dataclass
from typing import List, Optional
import re
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


def convert_numbered_pinyin_to_tones(pinyin: str) -> str:
    """Convert numbered pinyin (e.g., 'ni3hao3') to pinyin with tone marks (e.g., 'nǐhǎo')."""
    # Tone mark mappings for each vowel
    tone_marks = {
        'a': ['a', 'ā', 'á', 'ǎ', 'à'],
        'e': ['e', 'ē', 'é', 'ě', 'è'],
        'i': ['i', 'ī', 'í', 'ǐ', 'ì'],
        'o': ['o', 'ō', 'ó', 'ǒ', 'ò'],
        'u': ['u', 'ū', 'ú', 'ǔ', 'ù'],
        'ü': ['ü', 'ǖ', 'ǘ', 'ǚ', 'ǜ'],
        'v': ['v', 'ǖ', 'ǘ', 'ǚ', 'ǜ'],  # v is sometimes used for ü
        'A': ['A', 'Ā', 'Á', 'Ǎ', 'À'],
        'E': ['E', 'Ē', 'É', 'Ě', 'È'],
        'I': ['I', 'Ī', 'Í', 'Ǐ', 'Ì'],
        'O': ['O', 'Ō', 'Ó', 'Ǒ', 'Ò'],
        'U': ['U', 'Ū', 'Ú', 'Ǔ', 'Ù'],
        'Ü': ['Ü', 'Ǖ', 'Ǘ', 'Ǚ', 'Ǜ'],
        'V': ['V', 'Ǖ', 'Ǘ', 'Ǚ', 'Ǜ']  # V is sometimes used for Ü
    }
    
    def replace_syllable(match):
        syllable = match.group(1)
        tone = int(match.group(2))
        
        if tone == 5 or tone == 0:  # Neutral tone
            return syllable
        
        if tone > 5 or tone < 1:  # Invalid tone, return as-is
            return match.group(0)
        
        # Find the vowel to apply the tone mark to (case insensitive)
        # Priority: a > e > ou > o > i/u (whichever comes last)
        syllable_lower = syllable.lower()
        
        if 'a' in syllable_lower:
            vowel = 'a'
            pos = syllable_lower.index('a')
        elif 'e' in syllable_lower:
            vowel = 'e'
            pos = syllable_lower.index('e')
        elif 'ou' in syllable_lower:
            vowel = 'o'
            pos = syllable_lower.index('o')
        elif 'o' in syllable_lower:
            vowel = 'o'
            pos = syllable_lower.index('o')
        elif 'i' in syllable_lower and 'u' in syllable_lower:
            # Choose the one that comes last
            i_pos = syllable_lower.rindex('i')
            u_pos = syllable_lower.rindex('u')
            if i_pos > u_pos:
                vowel = 'i'
                pos = i_pos
            else:
                vowel = 'u'
                pos = u_pos
        elif 'i' in syllable_lower:
            vowel = 'i'
            pos = syllable_lower.rindex('i')
        elif 'u' in syllable_lower:
            vowel = 'u'
            pos = syllable_lower.rindex('u')
        elif 'ü' in syllable_lower or 'v' in syllable_lower:
            vowel = 'ü' if 'ü' in syllable_lower else 'v'
            pos = syllable_lower.index(vowel)
        else:
            return syllable  # No vowel found, return as is
        
        # Get the original vowel to preserve case
        original_vowel = syllable[pos]
        
        # Use the original vowel (with case) as the key for tone marks
        tone_key = original_vowel if original_vowel in tone_marks else vowel
        
        # Replace the vowel with the toned version
        if tone_key in tone_marks and tone < len(tone_marks[tone_key]):
            toned_vowel = tone_marks[tone_key][tone]
            return syllable[:pos] + toned_vowel + syllable[pos + 1:]
        
        return syllable
    
    # Pattern to match syllables with tone numbers (including 0)
    pattern = r'([a-züvA-ZÜVA-Z]+?)([0-5])'
    result = re.sub(pattern, replace_syllable, pinyin)
    
    return result


def pleco_to_anki(pleco_entry: PlecoEntry) -> AnkiCard:
    """Convert a PlecoEntry to an AnkiCard."""
    return AnkiCard(
        pinyin=convert_numbered_pinyin_to_tones(pleco_entry.pinyin),
        simplified=pleco_entry.chinese,
        meaning=pleco_entry.definition
    )