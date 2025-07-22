Feature: Character Definition Cleanup
  As a Chinese language learner
  I want unwanted patterns removed from single character definitions
  So that the character meanings are clean and relevant for learning

  Background:
    Given I have the following test dictionary data:
      | Chinese | Pinyin | Definition |
      | 鸟 | diǎo | variant of 屌[diao3]/penis/bird/CL:隻\|只[zhi1],群[qun2]/(dialect) to pay attention to/(intensifier) damned/goddam |
      | 蛋 | dàn | variant of 蜑[Dan4]/egg/CL:個\|个[ge4],打[da2]/oval-shaped thing |
      | 棋 | qí | variant of 棋[qi2]/chess/chess-like game/a game of chess/CL:盤\|盘[pan2]/chess piece/CL:個\|个[ge4],顆\|颗[ke1]/variant of 棋[qi2] |
      | 鼓 | gǔ | old variant of 鼓[gu3]/drum/CL:通[tong4],面[mian4]/to drum/to strike/to rouse/to bulge/to swell |
      | 心 | xīn | heart/mind/intention/center/core/CL:顆\|颗[ke1],個\|个[ge4] |
      | 湖 | hú | lake/CL:個\|个[ge4],片[pian4] |
      | 山 | shān | mountain/hill/anything that resembles a mountain/CL:座[zuo4]/bundled straw in which silkworms spin cocoons/gable |

  Scenario: Remove CL classifier patterns from character definitions
    When I process the character definitions for cleanup
    Then the definition for "鸟" should be "penis/bird/(dialect) to pay attention to/(intensifier) damned/goddam"
    And the definition for "蛋" should be "egg/oval-shaped thing"
    And the definition for "棋" should be "chess/chess-like game/a game of chess/chess piece"
    And the definition for "心" should be "heart/mind/intention/center/core"
    And the definition for "湖" should be "lake"
    And the definition for "山" should be "mountain/hill/anything that resembles a mountain/bundled straw in which silkworms spin cocoons/gable"

  Scenario: Remove 'variant of X' patterns from character definitions
    When I process the character definitions for cleanup
    Then the definition for "鸟" should be "penis/bird/(dialect) to pay attention to/(intensifier) damned/goddam"
    And the definition for "蛋" should be "egg/oval-shaped thing"
    And the definition for "棋" should be "chess/chess-like game/a game of chess/chess piece"
    And the definition for "鼓" should be "drum/to drum/to strike/to rouse/to bulge/to swell"

  Scenario: Remove 'old variant of X' patterns from character definitions
    When I process the character definitions for cleanup
    Then the definition for "鼓" should be "drum/to drum/to strike/to rouse/to bulge/to swell"

  Scenario: Keep valid definitions unchanged when no cleanup patterns found
    When I process the character definitions for cleanup
    Then the definition for "心" should be "heart/mind/intention/center/core"
    And the definition for "湖" should be "lake"
    And the definition for "山" should be "mountain/hill/anything that resembles a mountain/bundled straw in which silkworms spin cocoons/gable"

  Scenario: Handle multiple cleanup patterns in single definition
    Given I have a character "棋" with definition "variant of 棋[qi2]/chess/chess-like game/a game of chess/CL:盤|盘[pan2]/chess piece/CL:個|个[ge4],顆|颗[ke1]/variant of 棋[qi2]"
    When I process the character definitions for cleanup
    Then the definition for "棋" should be "chess/chess-like game/a game of chess/chess piece"

  Scenario: Handle empty definitions after cleanup
    Given I have a character "变" with definition "variant of 變[bian4]"
    When I process the character definitions for cleanup
    Then the definition for "变" should be ""

  Scenario: Preserve definitions with CL patterns that are not classifiers
    Given I have a character "清" with definition "clear/distinct/quiet/just and honest/pure/to clear/to settle (accounts)/the Ch'ing or Qing dynasty (1644-1911)/surname Qing"
    When I process the character definitions for cleanup
    Then the definition for "清" should be "clear/distinct/quiet/just and honest/pure/to clear/to settle (accounts)/the Ch'ing or Qing dynasty (1644-1911)/surname Qing"

  Scenario: Remove traditional|simplified variant patterns
    Given I have a character "庄" with definition "variant of 莊|庄[zhuang1]/farm/village/serious"
    And I have a character "岁" with definition "variant of 歲|岁[sui4]/age/year"
    And I have a character "体" with definition "old variant of 體|体[ti3]/body/form"
    When I process the character definitions for cleanup
    Then the definition for "庄" should be "farm/village/serious"
    And the definition for "岁" should be "age/year"
    And the definition for "体" should be "body/form"

  Scenario: Handle standalone traditional|simplified variant patterns
    Given I have a character "庙" with definition "variant of 廟|庙[miao4]"
    And I have a character "历" with definition "old variant of 歷|历[li4]"
    When I process the character definitions for cleanup
    Then the definition for "庙" should be ""
    And the definition for "历" should be ""
