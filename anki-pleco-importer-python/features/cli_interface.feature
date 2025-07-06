Feature: Command Line Interface
  As a user
  I want to use the command line interface
  So that I can convert Pleco files easily from the terminal


  Scenario: Parse and display TSV file as Anki cards with tone marks
    Given I have the sample TSV file "import.tsv"
    When I run the command "anki-pleco-importer features/examples/import.tsv"
    Then the output should contain "Parsed 6 entries from features/examples/import.tsv:"
    And the output should contain "1. 迷上"
    And the output should contain "Pinyin: míshàng"
    And the output should contain "Meaning: to become fascinated with; to become obsessed with"