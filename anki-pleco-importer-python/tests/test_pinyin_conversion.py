"""Unit tests for pinyin tone conversion functionality."""

from anki_pleco_importer.chinese import convert_numbered_pinyin_to_tones
from anki_pleco_importer.pleco import pleco_to_anki, PlecoEntry


class TestPinyinConversion:
    """Test cases for pinyin tone conversion."""

    def test_single_syllable_all_tones(self):
        """Test single syllables with all five tones."""
        # Test with 'ma' syllable
        assert convert_numbered_pinyin_to_tones("ma1") == "mā"
        assert convert_numbered_pinyin_to_tones("ma2") == "má"
        assert convert_numbered_pinyin_to_tones("ma3") == "mǎ"
        assert convert_numbered_pinyin_to_tones("ma4") == "mà"
        assert convert_numbered_pinyin_to_tones("ma5") == "ma"  # neutral tone
        assert convert_numbered_pinyin_to_tones("ma0") == "ma"  # neutral tone alternative

    def test_vowel_priority_rules(self):
        """Test that tone marks are applied to correct vowels based on priority rules."""
        # a has highest priority
        assert convert_numbered_pinyin_to_tones("bai3") == "bǎi"
        assert convert_numbered_pinyin_to_tones("hao3") == "hǎo"

        # e has second priority
        assert convert_numbered_pinyin_to_tones("hei1") == "hēi"
        assert convert_numbered_pinyin_to_tones("mei2") == "méi"

        # ou combination
        assert convert_numbered_pinyin_to_tones("gou3") == "gǒu"
        assert convert_numbered_pinyin_to_tones("lou2") == "lóu"

        # o when not in ou
        assert convert_numbered_pinyin_to_tones("bo1") == "bō"

        # i and u - last one gets the tone
        assert convert_numbered_pinyin_to_tones("liu2") == "liú"  # u comes last
        assert convert_numbered_pinyin_to_tones("gui4") == "guì"  # i comes last

    def test_complex_multi_syllable_words(self):
        """Test complex multi-syllable words from the sample data."""
        assert convert_numbered_pinyin_to_tones("mi2shang4") == "míshàng"
        assert convert_numbered_pinyin_to_tones("shun4jian1zhuan3yi2") == "shùnjiānzhuǎnyí"
        assert convert_numbered_pinyin_to_tones("tao3ren2xi3huan5") == "tǎorénxǐhuan"
        assert convert_numbered_pinyin_to_tones("suan4wu2yi2ce4") == "suànwúyícè"
        assert convert_numbered_pinyin_to_tones("yin2chang4") == "yínchàng"
        assert convert_numbered_pinyin_to_tones("dong4tan5") == "dòngtan"

    def test_all_vowels_with_tones(self):
        """Test all vowels with different tone marks."""
        # Test a
        assert convert_numbered_pinyin_to_tones("da1") == "dā"
        assert convert_numbered_pinyin_to_tones("da2") == "dá"
        assert convert_numbered_pinyin_to_tones("da3") == "dǎ"
        assert convert_numbered_pinyin_to_tones("da4") == "dà"

        # Test e
        assert convert_numbered_pinyin_to_tones("de1") == "dē"
        assert convert_numbered_pinyin_to_tones("de2") == "dé"
        assert convert_numbered_pinyin_to_tones("de3") == "dě"
        assert convert_numbered_pinyin_to_tones("de4") == "dè"

        # Test i
        assert convert_numbered_pinyin_to_tones("di1") == "dī"
        assert convert_numbered_pinyin_to_tones("di2") == "dí"
        assert convert_numbered_pinyin_to_tones("di3") == "dǐ"
        assert convert_numbered_pinyin_to_tones("di4") == "dì"

        # Test o
        assert convert_numbered_pinyin_to_tones("do1") == "dō"
        assert convert_numbered_pinyin_to_tones("do2") == "dó"
        assert convert_numbered_pinyin_to_tones("do3") == "dǒ"
        assert convert_numbered_pinyin_to_tones("do4") == "dò"

        # Test u
        assert convert_numbered_pinyin_to_tones("du1") == "dū"
        assert convert_numbered_pinyin_to_tones("du2") == "dú"
        assert convert_numbered_pinyin_to_tones("du3") == "dǔ"
        assert convert_numbered_pinyin_to_tones("du4") == "dù"

    def test_umlaut_vowels(self):
        """Test ü vowel handling (sometimes written as v)."""
        assert convert_numbered_pinyin_to_tones("nü3") == "nǚ"
        assert convert_numbered_pinyin_to_tones("lü4") == "lǜ"
        assert convert_numbered_pinyin_to_tones("nv3") == "nǚ"  # v as ü
        assert convert_numbered_pinyin_to_tones("lv4") == "lǜ"  # v as ü

    def test_edge_cases(self):
        """Test edge cases and special scenarios."""
        # Empty string
        assert convert_numbered_pinyin_to_tones("") == ""

        # No tone numbers
        assert convert_numbered_pinyin_to_tones("hello") == "hello"

        # Mixed content
        assert convert_numbered_pinyin_to_tones("ni3hao3world") == "nǐhǎoworld"

        # Invalid tone numbers (should not crash)
        assert convert_numbered_pinyin_to_tones("ma9") == "ma9"  # Invalid tone, return as-is

        # Syllables without vowels
        assert convert_numbered_pinyin_to_tones("ng1") == "ng"  # No vowels to mark, tone number removed

    def test_consonant_clusters(self):
        """Test syllables with consonant clusters."""
        assert convert_numbered_pinyin_to_tones("zhi1") == "zhī"
        assert convert_numbered_pinyin_to_tones("chu2") == "chú"
        assert convert_numbered_pinyin_to_tones("shu3") == "shǔ"
        assert convert_numbered_pinyin_to_tones("zhu4") == "zhù"

    def test_diphthongs_and_triphthongs(self):
        """Test complex vowel combinations."""
        assert convert_numbered_pinyin_to_tones("ai1") == "āi"
        assert convert_numbered_pinyin_to_tones("ei2") == "éi"
        assert convert_numbered_pinyin_to_tones("ao3") == "ǎo"
        assert convert_numbered_pinyin_to_tones("ou4") == "òu"
        assert convert_numbered_pinyin_to_tones("iao3") == "iǎo"  # a gets the tone in iao
        assert convert_numbered_pinyin_to_tones("iou2") == "ióu"  # o gets the tone in iou

    def test_pleco_to_anki_integration(self):
        """Test that pleco_to_anki uses pinyin conversion correctly."""
        pleco_entry = PlecoEntry(chinese="你好", pinyin="ni3hao3", definition="hello")

        anki_card = pleco_to_anki(pleco_entry)

        assert anki_card.pinyin == "nǐhǎo"
        assert anki_card.simplified == "你好"
        assert anki_card.meaning == "hello"

    def test_case_preservation(self):
        """Test that case is preserved in conversion."""
        assert convert_numbered_pinyin_to_tones("Ma1") == "Mā"
        assert convert_numbered_pinyin_to_tones("MA1") == "MĀ"
        assert convert_numbered_pinyin_to_tones("Ni3Hao3") == "NǐHǎo"

    def test_multiple_numbers_in_string(self):
        """Test strings with multiple tone numbers."""
        assert convert_numbered_pinyin_to_tones("wo3ai4ni3") == "wǒàinǐ"
        assert convert_numbered_pinyin_to_tones("xie4xie4") == "xièxiè"
        assert convert_numbered_pinyin_to_tones("zai4jian4") == "zàijiàn"
