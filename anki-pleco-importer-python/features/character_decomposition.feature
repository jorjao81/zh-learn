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
    And the structure notes should be "氵 (三点水) (meaning) + 青 (qīng) (sound)"

  Scenario: Decompose semantic-semantic compound character
    Given I have a Chinese character "好"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 女        | woman   | semantic | 女字旁  |
      | 子        | child   | semantic | 子字旁  |
    And the structure notes should be "女 (女字旁) + 子 (子字旁)"

  Scenario: Decompose another semantic-phonetic compound
    Given I have a Chinese character "河"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 氵        | water   | semantic | 三点水  |
      | 可        | unknown | phonetic | kě      |
    And the structure notes should be "氵 (三点水) (meaning) + 可 (kě) (sound)"

  Scenario: Decompose character with woman radical
    Given I have a Chinese character "妈"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 女        | woman   | semantic | 女字旁  |
      | 马        | horse   | phonetic | mǎ      |
    And the structure notes should be "女 (女字旁) (meaning) + 马 (mǎ) (sound)"

  Scenario: Decompose sun and moon compound
    Given I have a Chinese character "明"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 日        | sun/day | semantic | 日字旁  |
      | 月        | moon    | semantic | 月字旁  |
    And the structure notes should be "日 (日字旁) + 月 (月字旁)"

  Scenario: Decompose person and tree compound
    Given I have a Chinese character "休"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin   |
      | 亻        | person  | semantic | 单人旁   |
      | 木        | tree    | semantic | 木字旁   |
    And the structure notes should be "亻 (单人旁) + 木 (木字旁)"

  Scenario: Decompose water and work compound
    Given I have a Chinese character "江"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 氵        | water   | semantic | 三点水  |
      | 工        | work    | phonetic | gōng    |
    And the structure notes should be "氵 (三点水) (meaning) + 工 (gōng) (sound)"

  Scenario: Decompose person and you compound
    Given I have a Chinese character "你"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 亻        | person  | semantic | 单人旁  |
      | 尔        | unknown | phonetic | ěr      |
    And the structure notes should be "亻 (单人旁) (meaning) + 尔 (ěr) (sound)"

  Scenario: Decompose complex character with heart radical
    Given I have a Chinese character "想"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 相        | unknown | phonetic | xiāng   |
      | 心        | heart   | semantic | 心字底  |
    And the structure notes should be "相 (xiāng) (sound) + 心 (心字底) (meaning)"

  Scenario: Decompose character with heart radical variant
    Given I have a Chinese character "懂"
    When I decompose it
    Then I should get the following components:
      | component | meaning | type     | pinyin  |
      | 忄        | heart   | semantic | 竖心旁  |
      | 董        | unknown | phonetic | dǒng    |
    And the structure notes should be "忄 (竖心旁) (meaning) + 董 (dǒng) (sound)"

  Scenario: Handle invalid input
    Given I have an invalid input "ab"
    When I try to decompose it
    Then I should get an error "Input must be a single Chinese character"

  Scenario: Handle empty input
    Given I have an empty input ""
    When I try to decompose it
    Then I should get an error "Input must be a single Chinese character"

  Scenario: Decompose 3-character word using dictionary lookup
    Given I have the following Anki export dictionary:
      | chinese | pinyin   | definition |
      | 学      | xue2     | to learn   |
      | 习      | xi2      | to practice|
      | 学习    | xue2xi2  | to study   |
      | 生      | sheng1   | to give birth |
      | 活      | huo2     | to live    |
      | 生活    | sheng1huo2| life      |
    When I decompose the 3-character word "学习生"
    Then I should get the structural decomposition "学习(xuéxí - to study) + 生(shēng - to give birth)"

  Scenario: Decompose 4-character word preferring 2+2 split
    Given I have the following Anki export dictionary:
      | chinese | pinyin     | definition |
      | 学      | xue2       | to learn   |
      | 习      | xi2        | to practice|
      | 学习    | xue2xi2    | to study   |
      | 生      | sheng1     | to give birth |
      | 活      | huo2       | to live    |
      | 生活    | sheng1huo2 | life       |
    When I decompose the 4-character word "学习生活"
    Then I should get the structural decomposition "学习(xuéxí - to study) + 生活(shēnghuó - life)"

  Scenario: Decompose 4-character word with 3+1 split when no 2+2 available
    Given I have the following Anki export dictionary:
      | chinese | pinyin     | definition |
      | 学      | xue2       | to learn   |
      | 习      | xi2        | to practice|
      | 生      | sheng1     | to give birth |
      | 学习生  | xue2xi2sheng1| study life |
    When I decompose the 4-character word "学习生活"
    Then I should get the structural decomposition "学习生(xuéxíshēng - study life) + 活(huó - to live/alive/living/work/workmanship)"

  Scenario: Decompose 5-character word preferring longest matches
    Given I have the following Anki export dictionary:
      | chinese | pinyin       | definition |
      | 学      | xue2         | to learn   |
      | 习      | xi2          | to practice|
      | 生      | sheng1       | to give birth |
      | 活      | huo2         | to live    |
      | 学习    | xue2xi2      | to study   |
      | 生活    | sheng1huo2   | life       |
      | 方      | fang1        | direction  |
      | 式      | shi4         | style      |
      | 方式    | fang1shi4    | method     |
    When I decompose the 5-character word "学习生活方"
    Then I should get the structural decomposition "学习(xuéxí - to study) + 生活(shēnghuó - life) + 方(fāng - direction)"

  Scenario: Decompose word with no dictionary matches falls back to individual characters
    Given I have the following Anki export dictionary:
      | chinese | pinyin | definition |
      | 不      | bu4    | not        |
      | 存      | cun2   | to exist   |
      | 在      | zai4   | to be at   |
    When I decompose the 3-character word "不存在"
    Then I should get the structural decomposition "不(bù - not) + 存(cún - to exist) + 在(zài - to be at)"

  Scenario: Decompose multicharacter word identifying components from Chinese 2 note type
    Given I have the following Anki export dictionary with mixed note types:
      | chinese | pinyin     | definition      | notetype  |
      | 灵      | ling2      | spirit/soul     | Chinese   |
      | 魂      | hun2       | soul            | Chinese   |
      | 伴      | ban4       | companion       | Chinese   |
      | 侣      | lv3        | companion       | Chinese   |
      | 伴侣    | ban4lv3    | partner/couple  | Chinese 2 |
    When I decompose the 4-character word "灵魂伴侣" using the Anki parser
    Then I should get the structural decomposition "灵 líng spirit/soul + 魂 hún soul + 伴侣 bànlǚ partner/couple"
