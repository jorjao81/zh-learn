# Project: Anki Pleco Importer

## Overview
This is a Python application that converts Pleco flashcard exports to Anki-compatible format for Chinese language learning. The application helps users seamlessly transfer their Pleco vocabulary to Anki for spaced repetition study.

## Instructions

For all features you develop, use the following workflow:
* Create a new branch for the feature
* Come up with clear gherkin scenarios that exemplify the feature
* Then implement the code changes
* Make sure all tests and commit hooks are passing
* Create a commit message, a push and a merge request

## Project Structure
- `src/anki_pleco_importer/` - Main application code
- `features/` - BDD test scenarios using Behave
- `tests/` - Unit tests
- `docs/` - Documentation

## Development Commands
- Install dependencies: `pip install -r requirements-dev.txt`
- Run tests: `pytest`
- Run BDD tests: `behave`
- Format code: `black src/ tests/`
- Type checking: `mypy src/`
- Lint code: `flake8 src/ tests/`
- Run application: `python -m anki_pleco_importer.cli`

## Key Features (Planned)
1. Parse Pleco flashcard export files
2. Convert to Anki-compatible CSV format
3. Handle Chinese characters, pinyin, and definitions
4. Support multiple export formats
5. Validate data integrity

## Testing Strategy
- Unit tests with pytest for core functionality
- BDD tests with behave for user scenarios
- BDD scenarios should always have all test data they need explicitly defined in them
- Type checking with mypy
- Code formatting with black
- Linting with flake8

## Dependencies
- click: CLI interface
- pandas: Data processing
- pydantic: Data validation
- behave: BDD testing
- pytest: Unit testing

## Additional instructions
- Follow a test-first strategy
- Avoid handling to many errors, let exceptions bubble up and crash the application
- Avoid generalising to much, keep the application simple instead
- Always confirm commit message and changes before commiting
- Always push after committing

## Anki
Each anki note generates 3 cards:
1. Only the chinese characters in front, everything in the back
2. Only the audio in the front, everything in the back
3. Only the definition in the front, everything in the back
