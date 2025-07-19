Feature: Download latest flash file from Google Drive
  As a user
  I want to download the most recently uploaded file starting with "flash-" from my Google Drive
  So that I can process the latest Pleco export without manual file management

  Background:
    Given I have Google Drive API credentials configured
    And my Google Drive contains the following files:
      | filename                    | upload_date         |
      | flash-vocabulary-2023.txt   | 2023-12-01 10:00:00 |
      | flash-grammar-2023.txt      | 2023-12-01 11:00:00 |
      | other-file.txt              | 2023-12-01 12:00:00 |
      | flash-latest-2023.txt       | 2023-12-01 13:00:00 |

  Scenario: Download the most recent flash file
    When I run the command "anki-pleco-importer download-from-drive"
    Then the file "flash-latest-2023.txt" should be downloaded to the current directory
    And the output should contain "Downloaded: flash-latest-2023.txt"

  Scenario: No flash files found
    Given my Google Drive contains only the following files:
      | filename       | upload_date         |
      | other-file.txt | 2023-12-01 12:00:00 |
      | random.txt     | 2023-12-01 13:00:00 |
    When I run the command "anki-pleco-importer download-from-drive"
    Then the command should exit with error code 1
    And the output should contain "No files starting with 'flash-' found in Google Drive"

  Scenario: Download to specific directory
    When I run the command "anki-pleco-importer download-from-drive --output-dir /tmp/downloads"
    Then the file "flash-latest-2023.txt" should be downloaded to "/tmp/downloads/"
    And the output should contain "Downloaded: flash-latest-2023.txt to /tmp/downloads/"
