Feature: Command Line Interface
  As a user
  I want to use the command line interface
  So that I can convert Pleco files easily from the terminal

  Scenario: Display help information
    When I run the command "anki-pleco-importer --help"
    Then the output should contain usage information
    And the output should contain available options

  Scenario: Display version information
    When I run the command "anki-pleco-importer --version"
    Then the output should contain the version number

  Scenario: Convert file using command line
    Given I have a Pleco export file "input.txt"
    When I run the command "anki-pleco-importer input.txt -o output.csv"
    Then the file "output.csv" should be created
    And the file "output.csv" should contain the converted data

  Scenario: Handle missing input file
    When I run the command "anki-pleco-importer nonexistent.txt"
    Then I should get an error about the missing file
    And the exit code should be non-zero

  Scenario: Use default output filename
    Given I have a Pleco export file "input.txt"
    When I run the command "anki-pleco-importer input.txt"
    Then the file "input_anki.csv" should be created