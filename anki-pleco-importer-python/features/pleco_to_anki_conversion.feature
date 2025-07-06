Feature: Convert Pleco flashcard exports to Anki format
  As a Chinese language learner
  I want to convert my Pleco flashcard exports to Anki format
  So that I can use spaced repetition study in Anki

  Background:
    Given I have the anki-pleco-importer application

  Scenario: Convert a simple Pleco export file
    Given I have a Pleco export file with the following content:
      """
      你好\thello\tnǐ hǎo
      谢谢\tthank you\txiè xie
      """
    When I convert the file to Anki format
    Then the output should be a valid Anki CSV file
    And the output should contain the following cards:
      | Front | Back | Pinyin |
      | 你好 | hello | nǐ hǎo |
      | 谢谢 | thank you | xiè xie |

  Scenario: Handle empty Pleco export file
    Given I have an empty Pleco export file
    When I convert the file to Anki format
    Then I should get an error message "No flashcards found in input file"

  Scenario: Validate output file format
    Given I have a valid Pleco export file
    When I convert the file to Anki format
    Then the output file should have CSV headers
    And the output file should be properly formatted for Anki import

  Scenario: Handle malformed Pleco export data
    Given I have a Pleco export file with malformed data:
      """
      你好\thello
      谢谢\tthank you\txiè xie\textra_field
      """
    When I convert the file to Anki format
    Then I should get a warning about inconsistent data format
    And the conversion should still proceed with available data

  Scenario: Convert file with special characters
    Given I have a Pleco export file with special characters:
      """
      "你好"\t"Hello, world!"\t"nǐ hǎo"
      书籍\tbook (formal)\tshū jí
      """
    When I convert the file to Anki format
    Then the output should preserve all special characters correctly
    And the quotes should be handled properly in the CSV format