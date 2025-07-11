Feature: Character decomposition analysis
  As a Chinese language learner
  I want to see the structural components of Chinese characters
  So that I can understand their composition and meaning relationships

  Background:
    Given the CharacterDecomposer is available

  Scenario: Decompose semantic-phonetic compound character
    Given I have a Chinese character "清"
    When I decompose it
    Then I should get the following components:
      | component | meaning     | type     | pinyin  |
      | 氵        | water       | semantic | 三点水  |
      | 青        | green/blue  | phonetic | qīng    |
    And the structure notes should be "Semantic-phonetic compound: 氵 (三点水) (meaning) + 青 (qīng) (sound)"

  Scenario: Decompose semantic-semantic compound character
    Given I have a Chinese character "好"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 女        | woman   | semantic | 女字旁  |
      | 子        | child   | semantic | 子字旁  |
    And the structure notes should be "Semantic-semantic compound: 女 (女字旁) + 子 (子字旁)"

  Scenario: Decompose another semantic-phonetic compound
    Given I have a Chinese character "河"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 氵        | water   | semantic | 三点水  |
      | 可        | unknown | phonetic | kě      |
    And the structure notes should be "Semantic-phonetic compound: 氵 (三点水) (meaning) + 可 (kě) (sound)"

  Scenario: Decompose character with woman radical
    Given I have a Chinese character "妈"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 女        | woman   | semantic | 女字旁  |
      | 马        | horse   | phonetic | mǎ      |
    And the structure notes should be "Semantic-phonetic compound: 女 (女字旁) (meaning) + 马 (mǎ) (sound)"

  Scenario: Decompose sun and moon compound
    Given I have a Chinese character "明"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 日        | sun/day | semantic | 日字旁  |
      | 月        | moon    | semantic | 月字旁  |
    And the structure notes should be "Semantic-semantic compound: 日 (日字旁) + 月 (月字旁)"

  Scenario: Decompose person and tree compound
    Given I have a Chinese character "休"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin   |
      | 亻        | person  | semantic | 单人旁   |
      | 木        | tree    | semantic | 木字旁   |
    And the structure notes should be "Semantic-semantic compound: 亻 (单人旁) + 木 (木字旁)"

  Scenario: Decompose water and work compound
    Given I have a Chinese character "江"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 氵        | water   | semantic | 三点水  |
      | 工        | work    | phonetic | gōng    |
    And the structure notes should be "Semantic-phonetic compound: 氵 (三点水) (meaning) + 工 (gōng) (sound)"

  Scenario: Decompose person and you compound
    Given I have a Chinese character "你"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 亻        | person  | semantic | 单人旁  |
      | 尔        | unknown | phonetic | ěr      |
    And the structure notes should be "Semantic-phonetic compound: 亻 (单人旁) (meaning) + 尔 (ěr) (sound)"

  Scenario: Decompose complex character with heart radical
    Given I have a Chinese character "想"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 相        | unknown | phonetic | xiāng   |
      | 心        | heart   | semantic | 心字底  |
    And the structure notes should be "Phonetic-semantic compound: 相 (xiāng) (sound) + 心 (心字底) (meaning)"

  Scenario: Decompose character with heart radical variant
    Given I have a Chinese character "懂"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 忄        | heart   | semantic | 竖心旁  |
      | 董        | unknown | phonetic | dǒng    |
    And the structure notes should be "Semantic-phonetic compound: 忄 (竖心旁) (meaning) + 董 (dǒng) (sound)"

  Scenario: Handle invalid input
    Given I have an invalid input "ab"
    When I try to decompose it
    Then I should get an error "Input must be a single Chinese character"

  Scenario: Handle empty input
    Given I have an empty input ""
    When I try to decompose it
    Then I should get an error "Input must be a single Chinese character"

  Scenario: Decompose simple character that returns single component
    Given I have a Chinese character "森"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 木        | tree    | semantic | 木字旁  |
    And the structure notes should be "Simple character: 森"