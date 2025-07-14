Feature: Convert Pleco entries to Anki cards
  As a Chinese language learner
  I want to convert Pleco flashcard entries to Anki cards
  So that I can use them in Anki with proper field mapping

  Background:
    Given the pleco_to_anki conversion function is available

  Scenario Outline: Convert Pleco entries with basic formatting
    Given I have the following Pleco entries:
      | chinese   | pinyin   | definition   |
      | <chinese> | <pinyin> | <definition> |
    When I convert them to Anki cards
    Then I should get the following Anki cards:
      | simplified | pinyin           | meaning           |
      | <chinese>  | <expected_pinyin> | <expected_meaning> |

    Examples: Simple definitions
      | chinese | pinyin              | definition                                         | expected_pinyin     | expected_meaning                                    |
      | 迷上    | mi2shang4           | to become fascinated with; to become obsessed with | míshàng             | to become fascinated with; to become obsessed with |
      | 瞬间转移 | shun4jian1zhuan3yi2 | teleportation                                      | shùnjiānzhuǎnyí     | teleportation                                       |
      | 讨人喜欢 | tao3ren2xi3huan5    | 1 to attract people's affection 2 charming 3 delightful | tǎorénxǐhuan | 1 to attract people's affection 2 charming 3 delightful |
      | 算无遗策 | suan4wu2yi2ce4      | F.E. make a well-conceived plan                    | suànwúyícè          | F.E. make a well-conceived plan                     |

    Examples: Parts of speech formatting
      | chinese | pinyin     | definition                          | expected_pinyin | expected_meaning                               |
      | 吟唱    | yin2chang4 | verb sing (a verse); chant         | yínchàng        | <b>verb</b> sing (a verse); chant             |
      | 遵循    | zun1xun2   | V. follow; abide by; adhere to     | zūnxún          | <b>verb</b> follow; abide by; adhere to       |

  Scenario Outline: Convert entries with domain markers and complex formatting
    Given I have the following Pleco entries:
      | chinese   | pinyin   | definition   |
      | <chinese> | <pinyin> | <definition> |
    When I convert them to Anki cards
    Then I should get the following Anki cards:
      | simplified | pinyin           | meaning           |
      | <chinese>  | <expected_pinyin> | <expected_meaning> |

    Examples: Domain markers
      | chinese | pinyin       | definition                                                                                                                                           | expected_pinyin | expected_meaning                                                                                                                                                                              |
      | 瞑目    | ming2mu4     | 1 to close one's eyes 2 (fig.) to be contented at the time of one's death (Dying without closing one's eyes would signify having unresolved grievances.) | míngmù          | 1 to close one's eyes 2 <span color="red">figurative</span> to be contented at the time of one's death (Dying without closing one's eyes would signify having unresolved grievances.) |
      | 冲击波  | chong1ji1bo1 | physics MET shock wave; blast wave LIT impact                                                                                                       | chōngjībō       | <span color="red">physics</span> MET shock wave; blast wave <span color="red">literary</span> impact                                                                                     |

    Examples: Idiom formatting
      | chinese  | pinyin           | definition                                     | expected_pinyin  | expected_meaning                                           |
      | 寡不敌众 | gua3bu4di2zhong4 | idiom hopelessly outnumbered; fight against hopeless odds | guǎbùdízhòng     | <b>idiom</b> hopelessly outnumbered; fight against hopeless odds |
      | 以泪洗面 | yi3lei4xi3mian4  | to bathe one's face in tears (idiom)         | yǐlèixǐmiàn      | <b>idiom</b> to bathe one's face in tears                         |

    Examples: Abbreviation handling
      | chinese | pinyin   | definition                                                                         | expected_pinyin | expected_meaning                         |
      | 化肥    | hua4fei2 | noun abbreviation = 22930176化学肥料hua4xue2fei2liao4化学肥料 chemical fertilizer | huàféi          | <b>noun</b> chemical fertilizer         |

  Scenario Outline: Convert entries with multiple meanings and parts of speech
    Given I have the following Pleco entries:
      | chinese   | pinyin   | definition   |
      | <chinese> | <pinyin> | <definition> |
    When I convert them to Anki cards
    Then I should get the following Anki cards:
      | simplified | pinyin           | meaning           |
      | <chinese>  | <expected_pinyin> | <expected_meaning> |

    Examples: Multiple parts of speech
      | chinese | pinyin  | definition                                                                                                                                                                                                                                                                                                                                                                                                                         | expected_pinyin | expected_meaning                                                                     |
      | 有益    | you3yi4 | verb benefit; be good for 有益健康 yǒuyì jiànkāng good for one's health 做一个有益于人民的人 zuò yī ge yǒuyì yú rénmín de rén be a person who is of value to the people 会谈对双方都有益。 Huìtán duì shuāngfāng dōu yǒu yì. The talks were beneficial to both sides.  adjective profitable; beneficial; useful 有益的格言 Yǒuyì de géyán good popular maxims 作出有益的贡献 zuò chū yǒuyì de gòngxiàn make valuable contributions | yǒuyì           | <b>verb</b> benefit; be good for\\n<b>adjective</b> profitable; beneficial; useful |

    Examples: Complex definitions with dialect markers
      | chinese | pinyin   | definition                                                                                                                                                                                                                                | expected_pinyin | expected_meaning                                                                         |
      | 后背    | hou4bei4 | noun 1 back (of the body) 他后背上长了个疮。 Tā hòu bèi shàng zhǎng le ge chuāng. He has a boil on his back. 2 dialect at the back; in the rear 从后背袭击敌人 Cóng hòubèi xíjī dírén attack the enemy from the rear | hòubèi          | <b>noun</b> 1 back (of the body) 2 <span color="red">dialect</span> at the back; in the rear |

  Scenario Outline: Convert entries and verify structural decomposition
    Given I have the following Pleco entries:
      | chinese   | pinyin   | definition   |
      | <chinese> | <pinyin> | <definition> |
    When I convert them to Anki cards
    Then I should get the following Anki cards:
      | simplified | pinyin           | structural_decomposition           |
      | <chinese>  | <expected_pinyin> | <expected_structural_decomposition> |

    Examples: Structural decomposition
      | chinese | pinyin   | definition | expected_pinyin | expected_structural_decomposition                                                                                                                                                                                                                                                                      |
      | 有益    | you3yi4  | verb benefit; be good for 有益健康 yǒuyì jiànkāng good for one's health 做一个有益于人民的人 zuò yī ge yǒuyì yú rénmín de rén be a person who is of value to the people 会谈对双方都有益。 Huìtán duì shuāngfāng dōu yǒu yì. The talks were beneficial to both sides.  adjective profitable; beneficial; useful 有益的格言 Yǒuyì de géyán good popular maxims 作出有益的贡献 zuò chū yǒuyì de gòngxiàn make valuable contributions | yǒuyì           | 有(yǒu - to have/there is/there are/to exist/to be) + 益(yì - benefit/profit/advantage/beneficial/to increase/to add/all the more)                                                                                                                                                              |
      | 后背    | hou4bei4 | bbb        | hòubèi          | 后(hòu - empress/queen/(archaic) monarch/ruler/back/behind/rear/afterwards/after/later/post-) + 背(bèi - to be burdened/to carry on the back or shoulder/the back of a body or object/to turn one's back/to hide something from/to learn by heart/to recite from memory/unlucky (slang)/hard of hearing |

  Scenario: Convert single character and enhance with multi-character examples from Anki export
    Given I have the following Pleco entry:
      | chinese | pinyin | definition |
      | 学      | xue2   | to learn; to study; to imitate |
    And I have the following multi-character words in the Anki export containing "学":
      | word | pinyin   | meaning |
      | 学习 | xue2xi2  | to learn, to study |
      | 学校 | xue2xiao4| school |
      | 学生 | xue2sheng1| student |
      | 大学 | da4xue2  | university |
    When I convert the Pleco entry to an Anki card with Anki export enhancement
    Then I should get an Anki card with examples:
      | example |
      | 学习 (xuéxí) - to learn, to study |
      | 学校 (xuéxiào) - school |
      | 学生 (xuéshēng) - student |
      | 大学 (dàxué) - university |

  Scenario: Convert single character with limited multi-character examples
    Given I have the following Pleco entry:
      | chinese | pinyin | definition |
      | 人      | ren2   | person; people; man |
    And I have the following multi-character words in the Anki export containing "人":
      | word | pinyin    | meaning |
      | 人们 | ren2men5  | people |
      | 工人 | gong1ren2 | worker |
    When I convert the Pleco entry to an Anki card with Anki export enhancement
    Then I should get an Anki card with examples:
      | example |
      | 人们 (rénmen) - people |
      | 工人 (gōngrén) - worker |

  Scenario: Convert single character with no multi-character examples available
    Given I have the following Pleco entry:
      | chinese | pinyin | definition |
      | 珍      | zhen1  | precious; rare; to treasure |
    And I have no multi-character words in the Anki export containing "珍"
    When I convert the Pleco entry to an Anki card with Anki export enhancement
    Then I should get an Anki card with no additional examples

  Scenario: Convert multi-character word should not add additional examples
    Given I have the following Pleco entry:
      | chinese | pinyin  | definition |
      | 学习    | xue2xi2 | to learn; to study |
    And I have the following multi-character words in the Anki export containing "学":
      | word | pinyin   | meaning |
      | 学校 | xue2xiao4| school |
      | 学生 | xue2sheng1| student |
    When I convert the Pleco entry to an Anki card with Anki export enhancement
    Then I should get an Anki card with no additional examples from the export
