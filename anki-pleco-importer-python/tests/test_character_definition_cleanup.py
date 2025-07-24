"""Test character definition cleanup functionality."""

from anki_pleco_importer.chinese import clean_character_definition


class TestCharacterDefinitionCleanup:
    """Test that character definition cleanup removes unwanted patterns."""

    def test_remove_cl_patterns(self):
        """Test that CL classifier patterns are removed."""
        definition = "heart/mind/intention/center/core/CL:顆|颗[ke1],個|个[ge4]"
        result = clean_character_definition(definition)
        assert result == "heart/mind/intention/center/core"

    def test_remove_variant_patterns(self):
        """Test that 'variant of X[pinyin]' patterns are removed."""
        definition = (
            "variant of 屌[diao3]/penis/bird/CL:隻|只[zhi1],群[qun2]/"
            "(dialect) to pay attention to/(intensifier) damned/goddam"
        )
        result = clean_character_definition(definition)
        assert result == "penis/bird/(dialect) to pay attention to/(intensifier) damned/goddam"

    def test_remove_old_variant_patterns(self):
        """Test that 'old variant of X[pinyin]' patterns are removed."""
        definition = "old variant of 鼓[gu3]/drum/CL:通[tong4],面[mian4]/to drum/to strike/" "to rouse/to bulge/to swell"
        result = clean_character_definition(definition)
        assert result == "drum/to drum/to strike/to rouse/to bulge/to swell"

    def test_multiple_patterns_in_single_definition(self):
        """Test that multiple unwanted patterns are all removed."""
        definition = (
            "variant of 棋[qi2]/chess/chess-like game/a game of chess/CL:盤|盘[pan2]/"
            "chess piece/CL:個|个[ge4],顆|颗[ke1]/variant of 棋[qi2]"
        )
        result = clean_character_definition(definition)
        assert result == "chess/chess-like game/a game of chess/chess piece"

    def test_standalone_variant_becomes_empty(self):
        """Test that a definition with only variant pattern becomes empty."""
        definition = "variant of 變[bian4]"
        result = clean_character_definition(definition)
        assert result == ""

    def test_standalone_old_variant_becomes_empty(self):
        """Test that a definition with only old variant pattern becomes empty."""
        definition = "old variant of 變[bian4]"
        result = clean_character_definition(definition)
        assert result == ""

    def test_preserve_valid_cl_patterns(self):
        """Test that CL patterns that are not classifiers are preserved."""
        definition = (
            "clear/distinct/quiet/just and honest/pure/to clear/to settle (accounts)/"
            "the Ch'ing or Qing dynasty (1644-1911)/surname Qing"
        )
        result = clean_character_definition(definition)
        assert result == definition  # Should remain unchanged

    def test_empty_definition(self):
        """Test that empty definition is handled gracefully."""
        definition = ""
        result = clean_character_definition(definition)
        assert result == ""

    def test_none_definition(self):
        """Test that None definition is handled gracefully."""
        definition = None
        result = clean_character_definition(definition)
        assert result is None

    def test_definition_without_unwanted_patterns(self):
        """Test that definitions without unwanted patterns remain unchanged."""
        definition = (
            "mountain/hill/anything that resembles a mountain/bundled straw in which silkworms spin cocoons/gable"
        )
        result = clean_character_definition(definition)
        assert result == definition

    def test_cl_pattern_in_middle_of_definition(self):
        """Test that CL patterns in the middle of definitions are removed."""
        definition = "egg/CL:個|个[ge4],打[da2]/oval-shaped thing"
        result = clean_character_definition(definition)
        assert result == "egg/oval-shaped thing"

    def test_variant_pattern_at_end_of_definition(self):
        """Test that variant patterns at the end are removed."""
        definition = "chess/chess-like game/variant of 棋[qi2]"
        result = clean_character_definition(definition)
        assert result == "chess/chess-like game"

    def test_multiple_cl_patterns(self):
        """Test that multiple CL patterns are all removed."""
        definition = "chess/CL:盤|盘[pan2]/chess piece/CL:個|个[ge4],顆|颗[ke1]"
        result = clean_character_definition(definition)
        assert result == "chess/chess piece"

    def test_multiple_variant_patterns(self):
        """Test that multiple variant patterns are all removed."""
        definition = "variant of 棋[qi2]/chess/variant of 象[xiang4]/piece"
        result = clean_character_definition(definition)
        assert result == "chess/piece"

    def test_cleanup_leftover_separators(self):
        """Test that cleanup properly handles leftover slashes."""
        definition = "/variant of 棋[qi2]/"
        result = clean_character_definition(definition)
        assert result == ""

    def test_complex_real_world_example(self):
        """Test with a complex real-world example from the CSV."""
        definition = (
            "variant of 屌[diao3]/penis/bird/CL:隻|只[zhi1],群[qun2]/"
            "(dialect) to pay attention to/(intensifier) damned/goddam"
        )
        result = clean_character_definition(definition)
        expected = "penis/bird/(dialect) to pay attention to/(intensifier) damned/goddam"
        assert result == expected

    def test_traditional_simplified_variant_patterns(self):
        """Test that traditional|simplified variant patterns are removed."""
        test_cases = [
            ("variant of 莊|庄[zhuang1]/farm/village/serious", "farm/village/serious"),
            ("variant of 歲|岁[sui4]/age/year", "age/year"),
            ("definition/variant of 莊|庄[zhuang1]/other meanings", "definition/other meanings"),
            ("old variant of 歲|岁[sui4]/time/era", "time/era"),
            ("variant of 體|体[ti3]/body/form", "body/form"),
            ("meaning/old variant of 廟|庙[miao4]/temple", "meaning/temple"),
        ]

        for definition, expected in test_cases:
            result = clean_character_definition(definition)
            assert result == expected, (
                f"Failed for {definition}: got {result}, expected {expected}"
            )

    def test_standalone_traditional_simplified_variants(self):
        """Test standalone traditional|simplified variant patterns become empty."""
        test_cases = ["variant of 莊|庄[zhuang1]", "old variant of 歲|岁[sui4]", "variant of 體|体[ti3]"]

        for definition in test_cases:
            result = clean_character_definition(definition)
            assert result == "", f"Expected empty for {definition}, got {result}"
