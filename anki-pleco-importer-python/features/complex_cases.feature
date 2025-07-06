Feature: Handle complex Pleco entries with detailed definitions
  As a Chinese language learner
  I want to convert complex Pleco entries with detailed definitions and examples
  So that I can preserve all the rich content in my Anki cards

  Scenario: Convert entry with multiple meanings and parts of speech
    Given I have the following Pleco entry:
      | chinese | pinyin  | definition                                                                                                                                                                                                                                                                                                                                                                                                                         |
      | 有益    | you3yi4 | verb benefit; be good for 有益健康 yǒuyì jiànkāng good for one's health 做一个有益于人民的人 zuò yī ge yǒuyì yú rénmín de rén be a person who is of value to the people 会谈对双方都有益。 Huìtán duì shuāngfāng dōu yǒu yì. The talks were beneficial to both sides.  adjective profitable; beneficial; useful 有益的格言 Yǒuyì de géyán good popular maxims 作出有益的贡献 zuò chū yǒuyì de gòngxiàn make valuable contributions |
    When I convert it to an Anki card
    Then I should get the following Anki card:
      | pinyin | simplified | meaning                                                                           |
      | yǒuyì  | 有益       | <b>verb</b> benefit; be good for\n<b>adjective</b> profitable; beneficial; useful |

  Scenario: Convert entry with figurative meanings and cultural context
    Given I have the following Pleco entries:
      | chinese | pinyin       | definition                                                                                                                                               |
      | 瞑目    | ming2mu4     | 1 to close one's eyes 2 (fig.) to be contented at the time of one's death (Dying without closing one's eyes would signify having unresolved grievances.) |
      | 冲击波  | chong1ji1bo1 | physics MET shock wave; blast wave LIT impact                                                                                                            |

    When I convert them to Anki cards
    Then I should get the following Anki cards:
      | simplified | pinyin       | meaning                                                                                                                                                                                |
      | 瞑目       | míngmù       | 1 to close one's eyes 2 <span color="red">figurative</span> to be contented at the time of one's death (Dying without closing one's eyes would signify having unresolved grievances.) |
      | 冲击波     | chōngjībō | <span color="red">physics</span> MET shock wave; blast wave <span color="red">literary</span> impact                                                                                   |


  Scenario: Convert idioms and parts of speech
    Given I have the following Pleco entries:
      | chinese  | pinyin           | definition                                                |
      | 寡不敌众 | gua3bu4di2zhong4 | idiom hopelessly outnumbered; fight against hopeless odds |
      | 以泪洗面 | yi3lei4xi3mian4  | to bathe one's face in tears (idiom)                      |
      | 遵循     | zun1xun2         | V. follow; abide by; adhere to                            |

    When I convert them to Anki cards
    Then I should get the following Anki cards:
      | simplified | pinyin       | meaning                                                   |
      | 寡不敌众   | guǎbùdízhòng | idiom hopelessly outnumbered; fight against hopeless odds |
      | 以泪洗面   | yǐlèixǐmiàn  | <b>idiom</b> to bathe one's face in tears                 |
      | 遵循       | zūnxún     | <b>verb</b> follow; abide by; adhere to                   |





