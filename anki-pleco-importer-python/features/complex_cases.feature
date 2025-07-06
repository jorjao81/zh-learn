Feature: Handle complex Pleco entries with detailed definitions
  As a Chinese language learner
  I want to convert complex Pleco entries with detailed definitions and examples
  So that I can preserve all the rich content in my Anki cards

  # Scenario: Convert entry with neutral tone handling
  #   Given I have the following Pleco entry:
  #     | chinese | pinyin    | definition                                                                                                                                                              |
  #     | 动弹    | dong4tan5 | verb move; stir 机器不动弹了。 Jīqì bù dòngtan le. The machine has stopped. 车里太挤, 动弹不得。 Chē lǐ tài jǐ, dòngtan bude. The bus was so crowded that nobody could move. or The bus was jam-packed. |
  #   When I convert it to an Anki card
  #   Then I should get the following Anki card:
  #     | pinyin  | simplified | meaning | examples                                                                                                                                                                |
  #     | dòngtan | 动弹       | <b>verb</b> move; stir | 机器不动弹了。 Jīqì bù dòngtan le. The machine has stopped.\n车里太挤, 动弹不得。 Chē lǐ tài jǐ, dòngtan bude. The bus was so crowded that nobody could move. or The bus was jam-packed. |

  Scenario: Convert entry with multiple meanings and parts of speech
    Given I have the following Pleco entry:
      | chinese | pinyin  | definition                                                                                                                                                                                                                                                                                                                                                                     |
      | 有益    | you3yi4 | verb benefit; be good for 有益健康 yǒuyì jiànkāng good for one's health 做一个有益于人民的人 zuò yī ge yǒuyì yú rénmín de rén be a person who is of value to the people 会谈对双方都有益。 Huìtán duì shuāngfāng dōu yǒu yì. The talks were beneficial to both sides.  adjective profitable; beneficial; useful 有益的格言 Yǒuyì de géyán good popular maxims 作出有益的贡献 zuò chū yǒuyì de gòngxiàn make valuable contributions |
    When I convert it to an Anki card
    Then I should get the following Anki card:
      | pinyin | simplified | meaning |
      | yǒuyì  | 有益       | <b>verb</b> benefit; be good for\n<b>adjective</b> profitable; beneficial; useful | 
  # Scenario: Convert entry with figurative meanings and cultural context
  #   Given I have the following Pleco entry:
  #     | chinese | pinyin   | definition                                                                                                                                               |
  #     | 瞑目    | ming2mu4 | 1 to close one's eyes 2 (fig.) to be contented at the time of one's death (Dying without closing one's eyes would signify having unresolved grievances.) |
  #   When I convert it to an Anki card
  #   Then I should get the following Anki card:
  #     | pinyin | simplified | meaning                                                                                                                                                  |
  #     | míngmù | 瞑目       | 1 to close one's eyes 2 (fig.) to be contented at the time of one's death (Dying without closing one's eyes would signify having unresolved grievances.) |

  # Scenario: Convert four-character idiom
  #   Given I have the following Pleco entry:
  #     | chinese  | pinyin          | definition                            |
  #     | 以泪洗面 | yi3lei4xi3mian4 | to bathe one's face in tears (idiom) |
  #   When I convert it to an Anki card
  #   Then I should get the following Anki card:
  #     | pinyin      | simplified | meaning                               |
  #     | yǐlèixǐmiàn | 以泪洗面   | to bathe one's face in tears (idiom) |

  # Scenario: Convert specialized vocabulary with domain terms
  #   Given I have the following Pleco entry:
  #     | chinese | pinyin | definition                                                                |
  #     | 腹地    | fu4di4 | noun hinterland; interior 深入腹地 shēnrù fùdì invade deep into the hinterland |
  #   When I convert it to an Anki card
  #   Then I should get the following Anki card:
  #     | pinyin | simplified | meaning                                                                   |
  #     | fùdì   | 腹地       | noun hinterland; interior 深入腹地 shēnrù fùdì invade deep into the hinterland |