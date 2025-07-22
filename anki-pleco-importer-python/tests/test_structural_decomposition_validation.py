"""Tests for structural decomposition validation rules."""

from anki_pleco_importer.chinese import get_structural_decomposition_semantic, get_structural_decomposition


class TestStructuralDecompositionValidation:
    """Test that structural decomposition always follows proper validation rules."""

    def test_ziyiweishi_decomposition_should_not_copy_itself(self):
        """Test that 自以为是 is not decomposed to itself as a single component."""
        # Create a mock dictionary that contains ONLY the full word (worst case scenario)
        anki_dictionary = {"自以为是": {"pinyin": "zi4yi3wei2shi4", "definition": "consider oneself (always) in the right"}}

        # Test semantic version
        result_semantic = get_structural_decomposition_semantic("自以为是", anki_dictionary)
        print(f"Semantic result: {result_semantic}")

        # Should NOT be a single component showing the word itself
        assert "<ul>" in result_semantic, "Should have multiple components in a list"
        assert result_semantic.count("<li>") >= 2, "Should have at least 2 list items"

        # Should not contain the full word as a single component
        assert "自以为是</span>" not in result_semantic, "Should not contain the full word as single component"

        # Test non-semantic version
        result_plain = get_structural_decomposition("自以为是", anki_dictionary)
        print(f"Plain result: {result_plain}")

        # Should contain multiple components joined by +
        assert "+" in result_plain, "Should have multiple components joined by +"
        assert result_plain.count("+") >= 1, "Should have at least one + separator"

        # Should not start with the full word
        assert not result_plain.startswith("自以为是("), "Should not start with the full word"

    def test_any_multichar_word_always_has_multiple_components(self):
        """Test that any multi-character word always gets decomposed into multiple components."""
        test_cases = [
            "自以为是",  # 4 characters
            "研究生",  # 3 characters
            "大学生",  # 3 characters
        ]

        # Empty dictionary - should force fallback to character-by-character
        empty_dict = {}

        for word in test_cases:
            # Test semantic version
            result_semantic = get_structural_decomposition_semantic(word, empty_dict)

            # Must have multiple components
            if len(word) > 1:
                assert "<ul>" in result_semantic, f"Word '{word}' should have multiple components in a list"
                assert result_semantic.count("<li>") >= 2, f"Word '{word}' should have at least 2 components"

            # Test non-semantic version
            result_plain = get_structural_decomposition(word, empty_dict)

            # Must have multiple components
            if len(word) > 1:
                assert "+" in result_plain, f"Word '{word}' should have multiple components joined by +"

    def test_dictionary_lookup_forces_multicomponent_decomposition(self):
        """Test that even when full word is in dictionary, we still decompose it into multiple parts."""
        # Dictionary with the full word and its components
        dictionary = {
            "自以为是": {"pinyin": "zi4yi3wei2shi4", "definition": "consider oneself always right"},
            "自": {"pinyin": "zi4", "definition": "self"},
            "以": {"pinyin": "yi3", "definition": "with; by"},
            "为": {"pinyin": "wei2", "definition": "as; for"},
            "是": {"pinyin": "shi4", "definition": "is; correct"},
        }

        result_semantic = get_structural_decomposition_semantic("自以为是", dictionary)

        # Even though the full word is in dictionary, should still decompose it
        assert "<ul>" in result_semantic
        assert result_semantic.count("<li>") >= 2

        # Should contain individual characters or meaningful sub-components
        assert (
            "自" in result_semantic and "以" in result_semantic and "为" in result_semantic and "是" in result_semantic
        ), "Should contain the individual characters"

    def test_single_characters_can_be_decomposed(self):
        """Test that single characters can be decomposed into their components."""
        result = get_structural_decomposition_semantic("学", {})

        # Single characters might be decomposed into their components, which is fine
        # This test is just to confirm our validation doesn't break single character handling
        assert result is not None and result != ""  # Should return some result

        # If it's a simple character, it might not decompose (that's ok)
        # If it's a compound character, it should decompose (that's also ok)
        # The key is we don't enforce multiple components for single characters
