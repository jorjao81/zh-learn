"""Test for medicine domain marker functionality."""

from anki_pleco_importer.pleco import _format_meaning_with_html, _format_meaning_with_semantic_markup


class TestMedicineDomainMarker:
    """Test that medicine domain marker is properly recognized and formatted."""

    def test_medicine_domain_marker_html_formatting(self):
        """Test that medicine domain marker gets red color formatting."""
        meanings = ["medicine the study of treating diseases"]

        result = _format_meaning_with_html(meanings)

        # Should contain the red-colored medicine marker
        assert '<span style="color: red;">medicine</span>' in result
        assert "the study of treating diseases" in result

    def test_medicine_domain_marker_semantic_formatting(self):
        """Test that medicine domain marker gets semantic class."""
        meanings = ["medicine the study of treating diseases"]

        result = _format_meaning_with_semantic_markup(meanings)

        # Should contain the semantic domain class
        assert '<span class="domain">medicine</span>' in result
        assert "the study of treating diseases" in result

    def test_medicine_case_insensitive(self):
        """Test that medicine domain marker works case-insensitively."""
        test_cases = ["Medicine medical practice", "MEDICINE clinical research", "medicine pharmaceutical study"]

        for meaning in test_cases:
            # Test HTML formatting
            result_html = _format_meaning_with_html([meaning])
            assert (
                '<span style="color: red;">medicine</span>' in result_html.lower()
                or '<span style="color: red;">Medicine</span>' in result_html
                or '<span style="color: red;">MEDICINE</span>' in result_html
            )

            # Test semantic formatting
            result_semantic = _format_meaning_with_semantic_markup([meaning])
            assert (
                '<span class="domain">medicine</span>' in result_semantic.lower()
                or '<span class="domain">Medicine</span>' in result_semantic
                or '<span class="domain">MEDICINE</span>' in result_semantic
            )

    def test_medicine_word_boundary(self):
        """Test that medicine only matches as complete word, not as substring."""
        # Should match
        meanings_match = ["medicine studies diseases", "clinical medicine research", "medicine, the healing art"]

        for meaning in meanings_match:
            result = _format_meaning_with_semantic_markup([meaning])
            assert '<span class="domain">medicine</span>' in result.lower()

        # Should NOT match (as substring)
        meanings_no_match = [
            "medicinal herbs for healing",  # medicinal contains medicine but shouldn't match
            "biomedicine advanced research",  # compound word shouldn't match
        ]

        for meaning in meanings_no_match:
            result = _format_meaning_with_semantic_markup([meaning])
            # Should not contain the domain span for medicine
            assert '<span class="domain">medicine</span>' not in result.lower()

    def test_medicine_with_other_domain_markers(self):
        """Test that medicine works alongside other domain markers."""
        meaning = "biology and medicine both study living organisms"

        result = _format_meaning_with_semantic_markup([meaning])

        # Should contain both domain markers
        assert '<span class="domain">biology</span>' in result
        assert '<span class="domain">medicine</span>' in result
        assert "both study living organisms" in result
