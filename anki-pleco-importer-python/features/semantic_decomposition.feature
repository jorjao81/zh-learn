Feature: Handle semantic decomposition of expressions
  As a Chinese language learner


  Scenario: Convert entry with multiple meanings and parts of speech
    Given I have the following Pleco entry:
      | chinese | pinyin  | definition                                                                                                                                                                                                                                                                                                                                                                                                                         |
      | 有益    | you3yi4 | verb benefit; be good for 有益健康 yǒuyì jiànkāng good for one's health 做一个有益于人民的人 zuò yī ge yǒuyì yú rénmín de rén be a person who is of value to the people 会谈对双方都有益。 Huìtán duì shuāngfāng dōu yǒu yì. The talks were beneficial to both sides.  adjective profitable; beneficial; useful 有益的格言 Yǒuyì de géyán good popular maxims 作出有益的贡献 zuò chū yǒuyì de gòngxiàn make valuable contributions |
    When I convert it to an Anki card
    Then I should get the following Anki card:
      | pinyin | simplified | semantic_component                                                                           |
      | yǒuyì  | 有益       | 有(yǒu - to have/there is/there are/to exist/to be) + 益(yì - benefit/profit/advantage/beneficial/to increase/to add/all the more) |








