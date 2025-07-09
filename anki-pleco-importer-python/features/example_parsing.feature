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