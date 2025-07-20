"""Test cases for numbered definitions without part-of-speech tags."""

from src.anki_pleco_importer.pleco import parse_pleco_definition_semantic


class TestNumberedDefinitionsWithoutPOS:
    """Test numbered definitions are parsed correctly when no part-of-speech is present."""

    def test_simple_numbered_definitions(self):
        """Test simple numbered definitions like 三维."""
        definition = "1 three-dimensional 2 3D"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        expected = "<ol><li>three-dimensional</li><li>3D</li></ol>"
        assert meaning == expected

    def test_numbered_definitions_with_complex_meanings(self):
        """Test numbered definitions with more complex meanings."""
        definition = "1 back (of the body) 2 at the rear"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        expected = "<ol><li>back (of the body)</li><li>at the rear</li></ol>"
        assert meaning == expected

    def test_numbered_definitions_three_items(self):
        """Test numbered definitions with three items."""
        definition = "1 to learn 2 to study 3 to imitate"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        expected = "<ol><li>to learn</li><li>to study</li><li>to imitate</li></ol>"
        assert meaning == expected

    def test_current_behavior_documentation(self):
        """Document current behavior for 三维 to understand the bug."""
        definition = "1 three-dimensional 2 3D"
        meaning, examples, similar_chars = parse_pleco_definition_semantic(definition)

        print(f"三维 current output: {meaning}")

        # Check if it's correctly parsed as a list
        if not meaning.startswith("<ol>"):
            print("BUG CONFIRMED: numbered definitions should be parsed as ordered list")
            print("Expected: <ol><li>three-dimensional</li><li>3D</li></ol>")
            print(f"Got: {meaning}")
