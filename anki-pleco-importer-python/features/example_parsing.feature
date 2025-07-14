Feature: Parse examples from Pleco definitions
  As a Chinese language learner
  I want to extract usage examples from Pleco definitions
  So that I can see how words are used in context

  Background:
    Given the pleco_to_anki conversion function is available

  Scenario: Extract single example from definition
    Given I have a Pleco entry with definition "verb show filial respect to (one's elders) 他带了些南边的土产来孝敬他奶奶。 Tā dài le xiē nánbian de tǔchǎn lái xiàojìng tā nǎinai. He brought his grandmother some local produce from the south as a gift."
    When I convert it to an Anki card
    Then I should get the following examples:
      | example |
      | 他带了些南边的土产来孝敬他奶奶。 Tā dài le xiē nánbian de tǔchǎn lái xiàojìng tā nǎinai. He brought his grandmother some local produce from the south as a gift. |

  Scenario: Extract two examples separated by semicolon
    Given I have a Pleco entry with definition "noun virtue; moral excellence 美德无价。 měidé wújià. Virtue is beyond price. ; 诚实是一种美德。 Chéngshí shì yī zhǒng měidé. Honesty is a virtue."
    When I convert it to an Anki card
    Then I should get the following examples:
      | example |
      | 美德无价。 měidé wújià. Virtue is beyond price. |
      | 诚实是一种美德。 Chéngshí shì yī zhǒng měidé. Honesty is a virtue. |

  Scenario: Extract multiple examples from complex definition
    Given I have a Pleco entry with definition "verb perform; fulfill; carry out 履行合同 lǚxíng hétong fulfill a contract 履行诺言 lǚxíng nuòyán keep one's word 履行义务 lǚ xíng yì wù fulfill one's duty"
    When I convert it to an Anki card
    Then I should get the following examples:
      | example |
      | 履行合同 lǚxíng hétong fulfill a contract |
      | 履行诺言 lǚxíng nuòyán keep one's word |
      | 履行义务 lǚ xíng yì wù fulfill one's duty |

  Scenario: Extract examples with mixed formatting
    Given I have a Pleco entry with definition "adjective compunction; guilty 内疚于心 nèijiù yú xīn feel compunction 她托我的事没办成, 我深感内疚。 Tā tuō wǒ de shì méi bànchéng, wǒ shēngǎn nèijiù. I feel very bad because I failed to do what she wanted."
    When I convert it to an Anki card
    Then I should get the following examples:
      | example |
      | 内疚于心 nèijiù yú xīn feel compunction |
      | 她托我的事没办成, 我深感内疚。 Tā tuō wǒ de shì méi bànchéng, wǒ shēngǎn nèijiù. I feel very bad because I failed to do what she wanted. |

  Scenario: Extract examples across multiple meanings
    Given I have a Pleco entry with definition "noun 1 back (of the body) 他后背上长了个疮。 Tā hòu bèi shàng zhǎng le ge chuāng. He has a boil on his back. 2 dialect at the back 从后背袭击敌人 Cóng hòubèi xíjī dírén attack the enemy from the rear"
    When I convert it to an Anki card
    Then I should get the following examples:
      | example |
      | 他后背上长了个疮。 Tā hòu bèi shàng zhǎng le ge chuāng. He has a boil on his back. |
      | 从后背袭击敌人 Cóng hòubèi xíjī dírén attack the enemy from the rear |

  Scenario: Extract examples with periods and semicolons
    Given I have a Pleco entry with definition "verb 1 thunder 2 be thunderous 雷鸣电闪。 Léimíng diànshǎn. It's thundering and lightning. ; 雷鸣般的掌声 Léimíng bān de zhǎngshēng thunderous applause"
    When I convert it to an Anki card
    Then I should get the following examples:
      | example |
      | 雷鸣电闪。 Léimíng diànshǎn. It's thundering and lightning. |
      | 雷鸣般的掌声 Léimíng bān de zhǎngshēng thunderous applause |

  Scenario: Extract examples with sentence punctuation
    Given I have a Pleco entry with definition "verb fill up; stuff 往墙缝里填充水泥 wǎng qiáng fèng lǐ tiánchōng shuǐní fill the wall cracks with cement 她把枕头填充得很饱满。 Tā bǎ zhěntou tiánchōng de hěn bǎomǎn. She stuffed the pillow very full."
    When I convert it to an Anki card
    Then I should get the following examples:
      | example |
      | 往墙缝里填充水泥 wǎng qiáng fèng lǐ tiánchōng shuǐní fill the wall cracks with cement |
      | 她把枕头填充得很饱满。 Tā bǎ zhěntou tiánchōng de hěn bǎomǎn. She stuffed the pillow very full. |

  Scenario: No examples in definition
    Given I have a Pleco entry with definition "adjective simple; uncomplicated"
    When I convert it to an Anki card
    Then I should get the following examples:
      | example |

  Scenario: Examples embedded within numbered meanings
    Given I have a Pleco entry with definition "noun 1 foreign matter 食管异物 shíguǎn yìwù foreign body in the esophagus 2 literary rare object 奇珍异物 qízhēn yìwù rare treasures 3 literary dead person 化为异物 huàwéi yìwù give up the ghost"
    When I convert it to an Anki card
    Then I should get the following examples:
      | example |
      | 食管异物 shíguǎn yìwù foreign body in the esophagus |
      | 奇珍异物 qízhēn yìwù rare treasures |
      | 化为异物 huàwéi yìwù give up the ghost |

  Scenario: Examples with partial English translations
    Given I have a Pleco entry with definition "verb draw into; involve 卷入漩涡 Juǎnrù xuánwō sucked into a whirlpool 卷入一场纠纷 juǎnrù yī cháng jiūfēn get drawn into a dispute 他被卷入了这起丑闻。 Tā bèi juǎnrù le zhè qǐ chǒuwén. He got caught up in this scandal."
    When I convert it to an Anki card
    Then I should get the following examples:
      | example |
      | 卷入漩涡 Juǎnrù xuánwō sucked into a whirlpool |
      | 卷入一场纠纷 juǎnrù yī cháng jiūfēn get drawn into a dispute |
      | 他被卷入了这起丑闻。 Tā bèi juǎnrù le zhè qǐ chǒuwén. He got caught up in this scandal. |

  Scenario: Single character gets enhanced with multi-character examples from Anki export
    Given I have a Pleco entry with chinese "学", pinyin "xue2", and definition "to learn; to study; to imitate"
    And I have the following multi-character words in the Anki export containing "学":
      | word | pinyin     | meaning                |
      | 学习   | xue2xi2    | to learn, to study     |
      | 学校   | xue2xiao4  | school                 |
      | 学生   | xue2sheng1 | student                |
      | 大学   | da4xue2    | university             |
      | 数学   | shu4xue2   | mathematics            |
    When I convert the Pleco entry to an Anki card with Anki export enhancement
    Then I should get an Anki card with examples:
      | example |
      | 学习 (xuéxí) - to learn, to study |
      | 学校 (xuéxiào) - school |
      | 学生 (xuéshēng) - student |
      | 大学 (dàxué) - university |
      | 数学 (shùxué) - mathematics |

  Scenario: Single character with existing examples gets additional examples from Anki export
    Given I have a Pleco entry with chinese "人", pinyin "ren2", and definition "person; people; man 人人 rénrén everyone"
    And I have the following multi-character words in the Anki export containing "人":
      | word | pinyin    | meaning |
      | 人们   | ren2men5  | people  |
      | 工人   | gong1ren2 | worker  |
      | 主人   | zhu3ren2  | master, host |
    When I convert the Pleco entry to an Anki card with Anki export enhancement
    Then I should get an Anki card with examples:
      | example |
      | 人人 rénrén everyone |
      | 人们 (rénmen) - people |
      | 工人 (gōngrén) - worker |
      | 主人 (zhǔrén) - master, host |

  Scenario: Single character with no multi-character examples available
    Given I have a Pleco entry with chinese "珍", pinyin "zhen1", and definition "precious; rare; to treasure"
    And I have no multi-character words in the Anki export containing "珍"
    When I convert the Pleco entry to an Anki card with Anki export enhancement
    Then I should get an Anki card with no additional examples

  Scenario: Single character with limited examples from Anki export
    Given I have a Pleco entry with chinese "水", pinyin "shui3", and definition "water; liquid"
    And I have the following multi-character words in the Anki export containing "水":
      | word | pinyin     | meaning |
      | 水果   | shui3guo3  | fruit   |
      | 喝水   | he1shui3   | drink water |
    When I convert the Pleco entry to an Anki card with Anki export enhancement
    Then I should get an Anki card with examples:
      | example |
      | 水果 (shuǐguǒ) - fruit |
      | 喝水 (hēshuǐ) - drink water |

  Scenario: Single character with many examples gets limited to top 10
    Given I have a Pleco entry with chinese "的", pinyin "de5", and definition "possessive particle"
    And I have the following multi-character words in the Anki export containing "的":
      | word | pinyin     | meaning |
      | 我的   | wo3de5     | my, mine |
      | 你的   | ni3de5     | your, yours |
      | 他的   | ta1de5     | his |
      | 她的   | ta1de5     | her, hers |
      | 它的   | ta1de5     | its |
      | 我们的  | wo3men5de5 | our, ours |
      | 你们的  | ni3men5de5 | your, yours (plural) |
      | 他们的  | ta1men5de5 | their, theirs |
      | 真的   | zhen1de5   | really, truly |
      | 好的   | hao3de5    | good, okay |
      | 对的   | dui4de5    | correct, right |
      | 新的   | xin1de5    | new |
    When I convert the Pleco entry to an Anki card with Anki export enhancement
    Then I should get an Anki card with examples:
      | example |
      | 我的 (wǒde) - my, mine |
      | 你的 (nǐde) - your, yours |
      | 他的 (tāde) - his |
      | 她的 (tāde) - her, hers |
      | 它的 (tāde) - its |
      | 我们的 (wǒmende) - our, ours |
      | 你们的 (nǐmende) - your, yours (plural) |
      | 他们的 (tāmende) - their, theirs |
      | 真的 (zhēnde) - really, truly |
      | 好的 (hǎode) - good, okay |

  Scenario: Multi-character word should not get additional examples from Anki export
    Given I have a Pleco entry with chinese "学习", pinyin "xue2xi2", and definition "to learn; to study"
    And I have the following multi-character words in the Anki export containing "学":
      | word | pinyin     | meaning |
      | 学校   | xue2xiao4  | school |
      | 学生   | xue2sheng1 | student |
      | 大学   | da4xue2    | university |
    When I convert the Pleco entry to an Anki card with Anki export enhancement
    Then I should get an Anki card with no additional examples from the export
