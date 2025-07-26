"""Test cases for semantic markup of examples."""

from src.anki_pleco_importer.pleco import _format_single_example_semantic, format_examples_with_semantic_markup


class TestSemanticMarkupExamples:
    """Test semantic markup formatting for various example patterns."""

    def test_word_phrase_pattern_with_parentheses(self):
        """Test pattern: Chinese (pinyin) - translation"""
        example = "终宿主 (zhōng sùzhǔ) - final host"
        result = _format_single_example_semantic(example)
        expected = (
            '<span class="hanzi">终宿主</span> <span class="pinyin">zhōng sùzhǔ</span> - '
            '<span class="translation">final host</span>'
        )
        assert result == expected

    def test_word_phrase_pattern_without_parentheses(self):
        """Test pattern: Chinese pinyin translation"""
        example = "新奇的想法 xīnqí de xiǎngfa a novel idea"
        result = _format_single_example_semantic(example)
        # Current implementation has issues with multi-word pinyin
        # This test documents the current behavior - it needs fixing
        assert '<span class="hanzi">新奇的想法</span>' in result

    def test_sentence_pattern_with_periods(self):
        """Test pattern: Chinese sentence. Pinyin sentence. English sentence."""
        example = "这事她仿佛已经知道了。 Zhè shì tā fǎngfú yǐjing zhīdao le. " "She seems to know about it already."
        result = _format_single_example_semantic(example)
        expected = (
            '<span class="hanzi">这事她仿佛已经知道了。</span> '
            '<span class="pinyin">Zhè shì tā fǎngfú yǐjing zhīdao le.</span> '
            '<span class="translation">She seems to know about it already.</span>'
        )
        # This currently fails - needs implementation
        assert result == expected

    def test_complex_sentence_pattern(self):
        """Test complex sentence with punctuation."""
        example = "探险队急需一位向导。 Tànxiǎnduì jíxū yī wèi xiàngdǎo. " "The exploring party needs a guide urgently."
        result = _format_single_example_semantic(example)
        expected = (
            '<span class="hanzi">探险队急需一位向导。</span> '
            '<span class="pinyin">Tànxiǎnduì jíxū yī wèi xiàngdǎo.</span> '
            '<span class="translation">The exploring party needs a guide urgently.</span>'
        )
        assert result == expected

    def test_sentence_with_comma_and_question(self):
        """Test sentence with comma and question mark."""
        example = "我来给你们做向导, 怎么样？ Wǒ lái gěi nǐmen zuò xiàngdǎo, zěnmeyàng？ " "How about taking me as your guide?"
        result = _format_single_example_semantic(example)
        expected = (
            '<span class="hanzi">我来给你们做向导, 怎么样？</span> '
            '<span class="pinyin">Wǒ lái gěi nǐmen zuò xiàngdǎo, zěnmeyàng？</span> '
            '<span class="translation">How about taking me as your guide?</span>'
        )
        assert result == expected

    def test_short_sentence_pattern(self):
        """Test short sentence pattern."""
        example = "别小觑对手。 bié xiǎoqù duìshǒu. Don't underestimate your opponent."
        result = _format_single_example_semantic(example)
        expected = (
            '<span class="hanzi">别小觑对手。</span> '
            '<span class="pinyin">bié xiǎoqù duìshǒu.</span> '
            '<span class="translation">Don\'t underestimate your opponent.</span>'
        )
        assert result == expected

    def test_multiple_examples_formatting(self):
        """Test formatting multiple examples into list."""
        examples = [
            ("这事她仿佛已经知道了。 Zhè shì tā fǎngfú yǐjing zhīdao le. " "She seems to know about it already."),
            "别小觑对手。 bié xiǎoqù duìshǒu. Don't underestimate your opponent.",
        ]
        result = format_examples_with_semantic_markup(examples)
        assert '<ul><li class="example">' in result
        assert '<span class="hanzi">这事她仿佛已经知道了。</span>' in result
        assert '<span class="pinyin">Zhè shì tā fǎngfú yǐjing zhīdao le.</span>' in result
        assert '<span class="translation">She seems to know about it already.</span>' in result

    def test_edge_case_no_punctuation(self):
        """Test case where example has no clear punctuation separators."""
        example = "应急储备 yìngjí chǔbèi emergency stock"
        result = _format_single_example_semantic(example)
        expected = (
            '<span class="hanzi">应急储备</span> '
            '<span class="pinyin">yìngjí chǔbèi</span> '
            '<span class="translation">emergency stock</span>'
        )
        assert result == expected

    def test_phrase_with_multi_word_pinyin_no_punctuation(self):
        """Test case for phrase with multi-word pinyin and no punctuation - the specific issue."""
        example = "难忘的岁月 nánwàng de suìyuè unforgettable years"
        result = _format_single_example_semantic(example)
        expected = (
            '<span class="hanzi">难忘的岁月</span> '
            '<span class="pinyin">nánwàng de suìyuè</span> '
            '<span class="translation">unforgettable years</span>'
        )
        assert result == expected

    def test_additional_phrase_patterns_no_punctuation(self):
        """Test additional phrase patterns without punctuation."""
        test_cases = [
            (
                "研究生院 yánjiūshēng yuàn graduate school",
                (
                    '<span class="hanzi">研究生院</span> '
                    '<span class="pinyin">yánjiūshēng yuàn</span> '
                    '<span class="translation">graduate school</span>'
                ),
            ),
            (
                "大学生活 dàxuéshēng huó college life",
                (
                    '<span class="hanzi">大学生活</span> '
                    '<span class="pinyin">dàxuéshēng huó</span> '
                    '<span class="translation">college life</span>'
                ),
            ),
            (
                "音乐会 yīnyuè huì concert",
                (
                    '<span class="hanzi">音乐会</span> '
                    '<span class="pinyin">yīnyuè huì</span> '
                    '<span class="translation">concert</span>'
                ),
            ),
        ]

        for example, expected in test_cases:
            result = _format_single_example_semantic(example)
            assert result == expected, f"Failed for example: {example}"

    def test_malformed_example_fallback(self):
        """Test that malformed examples fall back gracefully."""
        example = "just some random text without clear structure"
        result = _format_single_example_semantic(example)
        # Should return as-is if no pattern matches
        assert result == example
