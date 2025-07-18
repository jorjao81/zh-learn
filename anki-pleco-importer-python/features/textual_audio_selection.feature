Feature: Textual Audio Selection Interface
  As a user
  I want to use a modern Textual interface for audio selection
  So that I can easily navigate and preview pronunciation options with keyboard controls

  Background:
    Given I have a Forvo API key configured
    And I have pronunciations available for Chinese words
    And the Textual audio selector is enabled

  Scenario: Navigate audio options with arrow keys
    Given I have 3 pronunciation options for the word "你好"
    When I open the Textual audio selection interface
    Then I should see a list with a skip option at the top
    And I should see 3 pronunciation options below the skip option
    And the first item should be highlighted by default
    When I press the down arrow key
    Then the second item should be highlighted
    When I press the up arrow key
    Then the first item should be highlighted again

  Scenario: Play audio preview with space key
    Given I have pronunciation options for the word "谢谢"
    And each pronunciation has a valid audio URL
    When I open the Textual audio selection interface
    And I navigate to a pronunciation option
    And I press the space key
    Then the audio file should be downloaded temporarily
    And the audio should be played through the system audio player
    And the interface should show "Played pronunciation by zhang123"

  Scenario: Select pronunciation with Enter key
    Given I have pronunciation options for the word "再见"
    When I open the Textual audio selection interface
    And I navigate to the second pronunciation option
    And I press the Enter key
    Then the selected pronunciation should be returned
    And the interface should close
    And the temporary preview files should be cleaned up

  Scenario: Skip all pronunciations
    Given I have pronunciation options for the word "学习"
    When I open the Textual audio selection interface
    And I navigate to the skip option at the top
    And I press the Enter key
    Then no pronunciation should be selected
    And the interface should close
    And the word should be marked as skipped

  Scenario: Skip with shortcut key
    Given I have pronunciation options for the word "工作"
    When I open the Textual audio selection interface
    And I press the 's' key
    Then no pronunciation should be selected
    And the interface should close
    And the word should be marked as skipped

  Scenario: Display pronunciation information correctly
    Given I have a pronunciation with the following data:
      | username | country | sex | votes | rating |
      | zhang123 | China   | f   | 5     | 4.2    |
    When I open the Textual audio selection interface
    Then I should see "🎵 zhang123 (♀ 🇨🇳) - 5 votes, rating: 4.2 ⭐⭐⭐⭐"

  Scenario: Handle audio download failure gracefully
    Given I have a pronunciation with an invalid audio URL
    When I open the Textual audio selection interface
    And I try to play the pronunciation
    Then I should see an error message "Could not download audio"
    And the interface should remain functional

  Scenario: Auto-select preferred user when available
    Given I have configured "native_speaker" as a preferred user
    And I have pronunciation options including one from "native_speaker"
    When I request audio selection for the word "北京"
    Then the pronunciation from "native_speaker" should be automatically selected
    And the Textual interface should not be shown

  Scenario: Show Textual interface when no preferred users available
    Given I have configured "preferred_user" as a preferred user
    And I have pronunciation options but none from "preferred_user"
    When I request audio selection for the word "上海"
    Then the Textual audio selection interface should be displayed
    And I should be able to manually select a pronunciation
