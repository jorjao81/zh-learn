"""
Tests for CharacterDecomposer module.
"""

import pytest
from anki_pleco_importer.character_decomposer import CharacterDecomposer, ComponentType


class TestCharacterDecomposer:
    """Test character decomposition functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.decomposer = CharacterDecomposer()

    def test_semantic_phonetic_compound(self):
        """Test semantic-phonetic compound character decomposition."""
        result = self.decomposer.decompose("清")

        assert result.character == "清"
        assert result.components == ["氵", "青"]
        assert result.radical_meanings == ["water", "green/blue"]
        assert result.component_types == [
            ComponentType.SEMANTIC,
            ComponentType.PHONETIC,
        ]
        assert result.component_pinyin == ["三点水", "qīng"]
        assert (
            "(meaning)" in result.structure_notes
            and "(sound)" in result.structure_notes
        )
        assert "青 (qīng)" in result.structure_notes

    def test_semantic_semantic_compound(self):
        """Test semantic-semantic compound character decomposition."""
        result = self.decomposer.decompose("好")

        assert result.character == "好"
        assert result.components == ["女", "子"]
        assert result.radical_meanings == ["woman", "child"]
        assert result.component_types == [
            ComponentType.SEMANTIC,
            ComponentType.SEMANTIC,
        ]
        assert result.component_pinyin == ["女字旁", "子字旁"]
        assert "女 (女字旁) + 子 (子字旁)" == result.structure_notes

    def test_complex_character(self):
        """Test complex character with multiple components."""
        result = self.decomposer.decompose("想")

        assert result.character == "想"
        assert len(result.components) == 2
        assert "heart" in result.radical_meanings
        assert ComponentType.SEMANTIC in result.component_types

    def test_invalid_input(self):
        """Test invalid input handling."""
        with pytest.raises(ValueError):
            self.decomposer.decompose("")

        with pytest.raises(ValueError):
            self.decomposer.decompose("ab")

    def test_component_classification(self):
        """Test component type classification."""
        # Test semantic radical classification
        assert self.decomposer._classify_component("氵", "清") == ComponentType.SEMANTIC
        assert self.decomposer._classify_component("女", "好") == ComponentType.SEMANTIC
        assert self.decomposer._classify_component("亻", "你") == ComponentType.SEMANTIC

        # Test phonetic component classification (default)
        assert self.decomposer._classify_component("青", "清") == ComponentType.PHONETIC
        assert self.decomposer._classify_component("工", "江") == ComponentType.PHONETIC

    def test_radical_meanings(self):
        """Test radical meaning lookup."""
        assert self.decomposer._get_radical_meaning("氵") == "water"
        assert self.decomposer._get_radical_meaning("女") == "woman"
        assert self.decomposer._get_radical_meaning("日") == "sun/day"
        assert self.decomposer._get_radical_meaning("月") == "moon"

    def test_pinyin_extraction(self):
        """Test pinyin extraction for phonetic components and Chinese names for semantic components."""
        # Test phonetic component pinyin extraction (should always use pinyin)
        assert (
            self.decomposer._get_component_pinyin("青", ComponentType.PHONETIC) == "qīng"
        )
        assert (
            self.decomposer._get_component_pinyin("工", ComponentType.PHONETIC) == "gōng"
        )
        assert (
            self.decomposer._get_component_pinyin("马", ComponentType.PHONETIC) == "mǎ"
        )

        # Test semantic component names (should use Chinese names for radicals)
        assert (
            self.decomposer._get_component_pinyin("氵", ComponentType.SEMANTIC) == "三点水"
        )
        assert (
            self.decomposer._get_component_pinyin("女", ComponentType.SEMANTIC) == "女字旁"
        )
        assert (
            self.decomposer._get_component_pinyin("日", ComponentType.SEMANTIC) == "日字旁"
        )
        assert (
            self.decomposer._get_component_pinyin("月", ComponentType.SEMANTIC) == "月字旁"
        )
