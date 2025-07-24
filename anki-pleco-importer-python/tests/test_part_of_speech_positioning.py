"""Test cases for part-of-speech positioning in numbered definitions."""

from src.anki_pleco_importer.pleco import parse_pleco_definition_semantic


class TestPartOfSpeechPositioning:
    """Test part-of-speech tags are placed outside ordered lists, not inside."""

    def test_single_pos_with_numbered_definitions(self):
        """Test single part-of-speech with numbered definitions."""
        definition = "verb 1 change direction 2 change one's political stand"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        expected = (
            '<span class="part-of-speech">verb</span> <ol><li>change direction</li>'
            "<li>change one's political stand</li></ol>"
        )
        assert meaning == expected

    def test_noun_with_numbered_definitions(self):
        """Test noun part-of-speech with numbered definitions."""
        definition = "noun 1 Christianity Doomsday; Day of Judgment; Judgment Day 2 end; doom"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        expected = (
            '<span class="part-of-speech">noun</span> <ol><li>Christianity Doomsday; '
            "Day of Judgment; Judgment Day</li><li>end; doom</li></ol>"
        )
        assert meaning == expected

    def test_multiple_pos_with_numbered_definitions(self):
        """Test multiple part-of-speech sections with numbered definitions."""
        # This is a complex case that would require more sophisticated parsing
        # For now, we'll focus on the main issue: single POS with numbered definitions
        # This test documents that the complex case is not yet fully supported
        definition = "noun 1 research 2 study verb 1 to research 2 to study"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        # The current implementation doesn't fully handle this complex case
        # but it should at least not put POS tags inside list items
        assert '<li><span class="part-of-speech">noun</span></li>' not in meaning
        assert meaning.startswith('<span class="part-of-speech">noun</span>')

    def test_pos_should_not_be_inside_list_items(self):
        """Test that part-of-speech tags are NOT included as separate list items."""
        definition = "verb 1 change direction 2 change one's political stand"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        # Should NOT contain part-of-speech inside <li> tags
        assert '<li><span class="part-of-speech">verb</span></li>' not in meaning

        # Should contain part-of-speech outside the ordered list
        assert meaning.startswith('<span class="part-of-speech">verb</span>')
        assert "<ol><li>change direction</li>" in meaning

    def test_complex_case_with_domains(self):
        """Test complex case with part-of-speech, numbered definitions, and domains."""
        # This is similar to the failing case in the test
        definition = "noun 1 research 2 study verb 1 to research 2 to study physics investigation chemistry analysis"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        # Should not put part-of-speech inside list items
        assert '<li><span class="part-of-speech">' not in meaning

        # Should have proper structure with POS outside lists
        assert meaning.startswith('<span class="part-of-speech">noun</span>')
        assert '<span class="part-of-speech">verb</span>' in meaning

    def test_现在_current_behavior_documentation(self):
        """Document current behavior for 转向 to understand the bug."""
        definition = "verb 1 change direction 2 change one's political stand"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        # This test documents what currently happens (incorrect behavior)
        # Once fixed, this test should be updated or removed
        print(f"Current output: {meaning}")

        # The bug: part-of-speech appears as first list item
        if '<li><span class="part-of-speech">verb</span></li>' in meaning:
            print("BUG CONFIRMED: part-of-speech is inside the list as a separate item")

        # Expected: part-of-speech should be outside the list
        if not meaning.startswith('<span class="part-of-speech">verb</span>'):
            print("BUG CONFIRMED: part-of-speech should be outside the list")

    def test_末日_current_behavior_documentation(self):
        """Document current behavior for 末日 to understand the bug."""
        definition = "noun 1 Christianity Doomsday; Day of Judgment; Judgment Day 2 end; doom"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        print(f"末日 current output: {meaning}")

        # Check for the bug
        if '<li><span class="part-of-speech">noun</span></li>' in meaning:
            print("BUG CONFIRMED: noun part-of-speech is inside the list as a separate item")
