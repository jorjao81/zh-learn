"""Test for zoology domain marker functionality."""

import pytest
from anki_pleco_importer.pleco import _format_meaning_with_html, _format_meaning_with_semantic_markup


class TestZoologyDomainMarker:
    """Test that zoology domain marker is properly recognized and formatted."""

    def test_zoology_domain_marker_html_formatting(self):
        """Test that zoology domain marker gets red color formatting."""
        meanings = ["zoology a mammal that feeds on fish"]

        result = _format_meaning_with_html(meanings)

        # Should contain the red-colored zoology marker
        assert '<span style="color: red;">zoology</span>' in result
        assert "a mammal that feeds on fish" in result

    def test_zoology_domain_marker_semantic_formatting(self):
        """Test that zoology domain marker gets semantic class."""
        meanings = ["zoology a mammal that feeds on fish"]

        result = _format_meaning_with_semantic_markup(meanings)

        # Should contain the semantic domain class
        assert '<span class="domain">zoology</span>' in result
        assert "a mammal that feeds on fish" in result

    def test_zoology_case_insensitive(self):
        """Test that zoology domain marker works case-insensitively."""
        test_cases = ["Zoology animal classification", "ZOOLOGY marine biology", "zoology bird behavior"]

        for meaning in test_cases:
            # Test HTML formatting
            result_html = _format_meaning_with_html([meaning])
            assert (
                '<span style="color: red;">zoology</span>' in result_html.lower()
                or '<span style="color: red;">Zoology</span>' in result_html
                or '<span style="color: red;">ZOOLOGY</span>' in result_html
            )

            # Test semantic formatting
            result_semantic = _format_meaning_with_semantic_markup([meaning])
            assert (
                '<span class="domain">zoology</span>' in result_semantic.lower()
                or '<span class="domain">Zoology</span>' in result_semantic
                or '<span class="domain">ZOOLOGY</span>' in result_semantic
            )

    def test_zoology_word_boundary(self):
        """Test that zoology only matches as complete word, not as substring."""
        # Should match
        meanings_match = ["zoology studies animals", "marine zoology research", "zoology, the study of animals"]

        for meaning in meanings_match:
            result = _format_meaning_with_semantic_markup([meaning])
            assert '<span class="domain">zoology</span>' in result.lower()

        # Should NOT match (as substring)
        meanings_no_match = [
            "zoologist studies animals",  # zoologist contains zoology but shouldn't match
            "paleozoology ancient animals",  # compound word shouldn't match
        ]

        for meaning in meanings_no_match:
            result = _format_meaning_with_semantic_markup([meaning])
            # Should not contain the domain span for zoology
            assert '<span class="domain">zoology</span>' not in result.lower()

    def test_zoology_with_other_domain_markers(self):
        """Test that zoology works alongside other domain markers."""
        meaning = "biology and zoology both study living organisms"

        result = _format_meaning_with_semantic_markup([meaning])

        # Should contain both domain markers
        assert '<span class="domain">biology</span>' in result
        assert '<span class="domain">zoology</span>' in result
        assert "both study living organisms" in result
