Feature: Convert Pleco entries to Anki cards
  As a Chinese language learner
  I want to convert Pleco flashcard entries to Anki cards
  So that I can use them in Anki with proper field mapping

  Background:
    Given the pleco_to_anki conversion function is available

  Scenario: Convert multiple Pleco entries to Anki cards with tone marks
    Given I have the following Pleco entries:
      | chinese    | pinyin              | definition                                                      |
      | 迷上       | mi2shang4           | to become fascinated with; to become obsessed with             |
      | 瞬间转移   | shun4jian1zhuan3yi2 | teleportation                                                   |
      | 讨人喜欢   | tao3ren2xi3huan5    | 1 to attract people's affection 2 charming 3 delightful        |
      | 算无遗策   | suan4wu2yi2ce4      | F.E. make a well-conceived plan                                 |
      | 吟唱       | yin2chang4          | verb sing (a verse); chant                                      |
    When I convert them to Anki cards
    Then I should get the following Anki cards:
      | pinyin              | simplified | meaning                                                         |
      | míshàng             | 迷上       | to become fascinated with; to become obsessed with             |
      | shùnjiānzhuǎnyí     | 瞬间转移   | teleportation                                                   |
      | tǎorénxǐhuan        | 讨人喜欢   | 1 to attract people's affection 2 charming 3 delightful        |
      | suànwúyícè          | 算无遗策   | F.E. make a well-conceived plan                                 |
      | yínchàng            | 吟唱       | <b>verb</b> sing (a verse); chant                                      |

