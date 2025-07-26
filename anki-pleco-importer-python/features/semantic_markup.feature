Feature: Semantic HTML markup for Anki cards
  As a Chinese language learner
  I want Anki cards to use semantic HTML markup without explicit formatting
  So that I can change presentation by just modifying CSS and easily extract meaningful information

  Background:
    Given the semantic markup conversion function is available

  Scenario Outline: Convert part-of-speech markers to semantic markup
    Given I have the following Pleco entries:
      | chinese   | pinyin   | definition   |
      | <chinese> | <pinyin> | <definition> |
    When I convert them to Anki cards with semantic markup
    Then I should get the following semantic HTML:
      | simplified | pinyin           | meaning           |
      | <chinese>  | <expected_pinyin> | <expected_meaning> |

    Examples: Part-of-speech markers
      | chinese | pinyin     | definition                          | expected_pinyin | expected_meaning                                                     |
      | 吟唱    | yin2chang4 | verb sing (a verse); chant         | yínchàng        | <span class="part-of-speech">verb</span> sing (a verse); chant     |
      | 遵循    | zun1xun2   | V. follow; abide by; adhere to     | zūnxún          | <span class="part-of-speech">verb</span> follow; abide by; adhere to |
      | 有益    | you3yi4    | noun benefit; adjective profitable | yǒuyì           | <span class="part-of-speech">noun</span> benefit; <span class="part-of-speech">adjective</span> profitable |

  Scenario Outline: Convert domain markers to semantic markup
    Given I have the following Pleco entries:
      | chinese   | pinyin   | definition   |
      | <chinese> | <pinyin> | <definition> |
    When I convert them to Anki cards with semantic markup
    Then I should get the following semantic HTML:
      | simplified | pinyin           | meaning           |
      | <chinese>  | <expected_pinyin> | <expected_meaning> |

    Examples: Domain markers
      | chinese | pinyin       | definition                                  | expected_pinyin | expected_meaning                                                                        |
      | 冲击波  | chong1ji1bo1 | physics shock wave; aerospace blast wave   | chōngjībō       | <span class="domain">physics</span> shock wave; <span class="domain">aerospace</span> blast wave |
      | 实验    | shi2yan4    | chemistry experiment; biology test        | shíyàn          | <span class="domain">chemistry</span> experiment; <span class="domain">biology</span> test |

  Scenario Outline: Convert usage markers to semantic markup
    Given I have the following Pleco entries:
      | chinese   | pinyin   | definition   |
      | <chinese> | <pinyin> | <definition> |
    When I convert them to Anki cards with semantic markup
    Then I should get the following semantic HTML:
      | simplified | pinyin           | meaning           |
      | <chinese>  | <expected_pinyin> | <expected_meaning> |

    Examples: Usage markers
      | chinese | pinyin    | definition                              | expected_pinyin | expected_meaning                                                                                            |
      | 古语    | gu3yu3    | literary ancient saying; dated phrase  | gǔyǔ            | <span class="usage literary">literary</span> ancient saying; <span class="usage dated">dated</span> phrase |
      | 俚语    | li3yu3    | colloquial slang; pejorative vulgar    | lǐyǔ            | <span class="usage colloquial">colloquial</span> slang; <span class="usage pejorative">pejorative</span> vulgar |

  Scenario Outline: Convert multiple definitions to HTML lists
    Given I have the following Pleco entries:
      | chinese   | pinyin   | definition   |
      | <chinese> | <pinyin> | <definition> |
    When I convert them to Anki cards with semantic markup
    Then I should get the following semantic HTML:
      | simplified | pinyin           | meaning           |
      | <chinese>  | <expected_pinyin> | <expected_meaning> |

    Examples: Multiple definitions
      | chinese | pinyin   | definition                           | expected_pinyin | expected_meaning                                                                                                                                                                                  |
      | 后背    | hou4bei4 | 1 back (of the body) 2 at the rear | hòubèi          | <ol><li>back (of the body)</li><li>at the rear</li></ol>                                                                                                                                        |
      | 学习    | xue2xi2  | 1 to learn 2 to study 3 to imitate | xuéxí           | <ol><li>to learn</li><li>to study</li><li>to imitate</li></ol>                                                                                                                                  |

  Scenario Outline: Convert multiple examples to HTML lists with semantic classes
    Given I have the following Pleco entries:
      | chinese   | pinyin   | definition   |
      | <chinese> | <pinyin> | <definition> |
    When I convert them to Anki cards with semantic markup
    Then I should get the following semantic HTML:
      | simplified | pinyin           | examples           |
      | <chinese>  | <expected_pinyin> | <expected_examples> |

    Examples: Multiple examples
      | chinese | pinyin  | definition                                                                                                                                    | expected_pinyin | expected_examples                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
      | 学习    | xue2xi2 | to learn; to study 学习中文 xue2xi2zhong1wen2 learn Chinese 我在学习 wo3zai4xue2xi2 I am studying 学习很重要 xue2xi2hen3zhong4yao4 studying is important | xuéxí           | <ul><li class="example"><span class="hanzi">学习中文</span> <span class="pinyin">xuéxízhōngwén</span> - <span class="translation">learn Chinese</span></li><li class="example"><span class="hanzi">我在学习</span> <span class="pinyin">wǒzàixuéxí</span> - <span class="translation">I am studying</span></li><li class="example"><span class="hanzi">学习很重要</span> <span class="pinyin">xuéxíhěnzhòngyào</span> - <span class="translation">studying is important</span></li></ul> |

  Scenario Outline: Convert character decomposition to semantic markup
    Given I have the following character decomposition:
      | character | components | radical_meanings | component_types | component_pinyin | structure_notes |
      | <character> | <components> | <radical_meanings> | <component_types> | <component_pinyin> | <structure_notes> |
    When I convert the decomposition to semantic markup
    Then I should get the following semantic HTML:
      | character | expected_decomposition |
      | <character> | <expected_decomposition> |

    Examples: Character decomposition
      | character | components | radical_meanings | component_types | component_pinyin | structure_notes | expected_decomposition |
      | 语       | ["讠", "吾"] | ["speech", "I/me"] | ["semantic", "phonetic"] | ["言字旁", "wú"] | 讠 言字旁 (meaning) + 吾 wú (sound) | <ul><li><span class="semantic">讠</span> <span class="pinyin">言字旁</span> - <span class="definition">speech</span></li><li><span class="phonetic">吾</span> <span class="pinyin">wú</span> - <span class="definition">I/me</span></li></ul> |
      | 江       | ["氵", "工"] | ["water", "work"] | ["semantic", "phonetic"] | ["三点水", "gōng"] | 氵 三点水 (meaning) + 工 gōng (sound) | <ul><li><span class="semantic">氵</span> <span class="pinyin">三点水</span> - <span class="definition">water</span></li><li><span class="phonetic">工</span> <span class="pinyin">gōng</span> - <span class="definition">work</span></li></ul> |

  Scenario Outline: Convert word decomposition to semantic markup
    Given I have the following word decomposition:
      | word | components | component_pinyin | component_definitions |
      | <word> | <components> | <component_pinyin> | <component_definitions> |
    When I convert the word decomposition to semantic markup
    Then I should get the following semantic HTML:
      | word | expected_decomposition |
      | <word> | <expected_decomposition> |

    Examples: Word decomposition
      | word | components | component_pinyin | component_definitions | expected_decomposition |
      | 学习 | ["学", "习"] | ["xué", "xí"] | ["to learn", "to practice"] | <ul><li><span class="hanzi">学</span> <span class="pinyin">xué</span> - <span class="definition">to learn</span></li><li><span class="hanzi">习</span> <span class="pinyin">xí</span> - <span class="definition">to practice</span></li></ul> |
      | 北京 | ["北", "京"] | ["běi", "jīng"] | ["north", "capital"] | <ul><li><span class="hanzi">北</span> <span class="pinyin">běi</span> - <span class="definition">north</span></li><li><span class="hanzi">京</span> <span class="pinyin">jīng</span> - <span class="definition">capital</span></li></ul> |

  Scenario Outline: Convert complex entries with all semantic markup features
    Given I have the following Pleco entries:
      | chinese   | pinyin   | definition   |
      | <chinese> | <pinyin> | <definition> |
    When I convert them to Anki cards with semantic markup
    Then I should get the following semantic HTML:
      | simplified | pinyin           | meaning           |
      | <chinese>  | <expected_pinyin> | <expected_meaning> |

    Examples: Complex entries with multiple features
      | chinese | pinyin   | definition                                                                                    | expected_pinyin | expected_meaning                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
      | 研究    | yan2jiu1 | noun 1 research 2 study verb 3 to research 4 to study physics investigation chemistry analysis | yánjiū          | <span class="part-of-speech">noun</span> <ol><li>research</li><li>study</li></ol> <span class="part-of-speech">verb</span> <ol><li>to research</li><li>to study</li></ol> <span class="domain">physics</span> investigation <span class="domain">chemistry</span> analysis |
