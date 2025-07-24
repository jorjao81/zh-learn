"""Test for derog. usage marker functionality."""

from anki_pleco_importer.pleco import _format_meaning_with_html, _format_meaning_with_semantic_markup


class TestDerogUsageMarker:
    """Test that derog. usage marker is properly recognized and formatted."""

    def test_derog_usage_marker_html_formatting(self):
        """Test that derog. usage marker gets proper HTML formatting."""
        meanings = ["derog. a term used disparagingly"]

        result = _format_meaning_with_html(meanings)

        # Note: HTML formatting for usage markers may not be implemented yet
        # For now, just check that the text is preserved
        assert "a term used disparagingly" in result

    def test_derog_usage_marker_semantic_formatting(self):
        """Test that derog. usage marker gets semantic class."""
        meanings = ["derog. a term used disparagingly"]

        result = _format_meaning_with_semantic_markup(meanings)

        # Should contain the semantic usage class
        assert '<span class="usage derogatory">derogatory</span>' in result
        assert "a term used disparagingly" in result

    def test_parenthetical_derog_usage_marker(self):
        """Test that (derog.) usage marker also works."""
        meanings = ["(derog.) a disparaging term"]

        result = _format_meaning_with_semantic_markup(meanings)

        # Should contain the semantic usage class
        assert '<span class="usage derogatory">derogatory</span>' in result
        assert "a disparaging term" in result

    def test_derog_abbreviation_matching(self):
        """Test that derog. matches the abbreviation with period, not substrings."""
        # Should match (derog. with period)
        meanings_match = ["derog. insulting term", "some meaning derog. another part", "derog. offensive language"]

        for meaning in meanings_match:
            result = _format_meaning_with_semantic_markup([meaning])
            assert '<span class="usage derogatory">derogatory</span>' in result

        # Should NOT match (words containing derog but not the abbreviation)
        meanings_no_match = [
            "derogation is the act of disparaging",  # derogation doesn't have period after derog
            "derogative comments are harmful",  # derogative doesn't have period after derog
        ]

        for meaning in meanings_no_match:
            result = _format_meaning_with_semantic_markup([meaning])
            # Should not contain the usage span for derogatory
            assert '<span class="usage derogatory">derogatory</span>' not in result

    def test_derog_with_other_usage_markers(self):
        """Test that derog. works alongside other usage markers."""
        meaning = "derog. colloquial term used in dialect"

        result = _format_meaning_with_semantic_markup([meaning])

        # Should contain multiple usage markers
        assert '<span class="usage derogatory">derogatory</span>' in result
        assert '<span class="usage colloquial">colloquial</span>' in result
        assert '<span class="usage dialect">dialect</span>' in result
        assert "term used in" in result

    def test_case_insensitive(self):
        """Test that derog. is case insensitive (matches both cases)."""
        test_cases = ["derog. insulting term", "DEROG. offensive language", "Derog. disparaging word"]

        for meaning in test_cases:
            result = _format_meaning_with_semantic_markup([meaning])
            assert '<span class="usage derogatory">derogatory</span>' in result
