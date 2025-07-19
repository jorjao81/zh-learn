Feature: Interactive Audio Selection with Arrow Navigation
  As a user converting Pleco flashcards
  I want to select pronunciation audio with arrow navigation
  So that I can easily choose the best pronunciation for each Chinese word


  Background:
    Given I have a Forvo API key configured
    And I have the sample TSV file "import.tsv" with word "你好"
    And Forvo returns multiple pronunciations for "你好":
      | username | gender | country | votes | rating |
      | native_speaker_1 | f | China | 15 | 4.5 |
      | native_speaker_2 | m | Taiwan | 8 | 4.2 |
      | learner_voice | f | United States | 3 | 3.1 |


  Scenario: Navigate audio options with arrow keys and auto-play
    Given I run the command "anki-pleco-importer convert features/examples/import.tsv --audio"
    When the audio selection interface appears for "你好"
    Then I should see a list of pronunciation options with:
      | Option | Display |
      | 1 | native_speaker_1 (♀ 🇨🇳) - 15 votes, rating: 4.5 ⭐⭐⭐⭐⭐ |
      | 2 | native_speaker_2 (♂ 🇹🇼) - 8 votes, rating: 4.2 ⭐⭐⭐⭐ |
      | 3 | learner_voice (♀ 🇺🇸) - 3 votes, rating: 3.1 ⭐⭐⭐ |
      | 4 | Skip this word |
    And the first option should be highlighted
    And I should see instructions "Use ↑↓ arrows to navigate (audio plays automatically), ENTER to select"
    And the audio for "native_speaker_1" should automatically play


  Scenario: Audio plays automatically when highlighting option
    Given I run the command "anki-pleco-importer convert features/examples/import.tsv --audio"
    And the audio selection interface appears for "你好"
    When I press the DOWN arrow to highlight "native_speaker_2"
    Then the audio for "native_speaker_2" should automatically play
    And I should see "🔊 native_speaker_2..." then "✅ native_speaker_2"
    And the interface should remain ready for selection


  Scenario: Select audio with Enter after auto-preview
    Given I run the command "anki-pleco-importer convert features/examples/import.tsv --audio"
    And the audio selection interface appears for "你好"
    When I press the DOWN arrow to highlight "native_speaker_2"
    And the audio plays automatically
    And I press ENTER to confirm selection
    Then the pronunciation by "native_speaker_2" should be selected
    And the interface should close
    And the conversion should continue


  Scenario: Navigate to skip option and select it
    Given I run the command "anki-pleco-importer convert features/examples/import.tsv --audio"
    And the audio selection interface appears for "你好"
    When I press the DOWN arrow 3 times to highlight "Skip this word"
    Then no audio should play (skip option highlighted)
    When I press ENTER
    Then no audio should be selected for "你好"
    And the interface should close
    And the conversion should continue


  Scenario: Cycle through options with arrow keys and auto-play
    Given I run the command "anki-pleco-importer convert features/examples/import.tsv --audio"
    And the audio selection interface appears for "你好"
    When I press the DOWN arrow 4 times
    Then the first option should be highlighted again
    And the audio for "native_speaker_1" should play again
    When I press the UP arrow
    Then the "Skip this word" option should be highlighted
    And no audio should play


  Scenario: Handle escape key to skip
    Given I run the command "anki-pleco-importer convert features/examples/import.tsv --audio"
    And the audio selection interface appears for "你好"
    When I press ESCAPE
    Then no audio should be selected for "你好"
    And the interface should close
    And the conversion should continue


  Scenario: Audio feedback during highlight navigation
    Given I run the command "anki-pleco-importer convert features/examples/import.tsv --audio"
    And the audio selection interface appears for "你好"
    When the first option is highlighted initially
    Then I should see "🔊 native_speaker_1..." then "✅ native_speaker_1"
    When I press the DOWN arrow to highlight "native_speaker_2"
    Then I should see "🔊 native_speaker_2..." then "✅ native_speaker_2"
    And the interface should be ready for selection


  Scenario: Avoid replaying same audio when not moving
    Given I run the command "anki-pleco-importer convert features/examples/import.tsv --audio"
    And the audio selection interface appears for "你好"
    And the audio for "native_speaker_1" plays automatically
    When I press some other key that doesn't change selection
    Then the audio for "native_speaker_1" should not play again
