# Anki Pleco Importer

A Python application to convert Pleco flashcard exports to Anki-compatible format for Chinese language learning.

## Features

- Convert Pleco flashcard exports to Anki CSV format
- Preserve Chinese characters, pinyin, and definitions
- Support for multiple export formats
- Data validation and integrity checks
- Command-line interface for easy usage

## AnkiCard Model

The application uses an `AnkiCard` model to represent flashcards with the following fields:

- **pinyin**: The pinyin romanization of the Chinese word
- **simplified**: The word using simplified Chinese characters
- **pronunciation**: Audio file path for pronunciation (optional)
- **meaning**: The definition/meaning of the word
- **examples**: List of usage examples (optional)
- **phonetic_component**: Phonetic component of the character (optional)
- **semantic_component**: Semantic component of the character (optional)
- **similar_characters**: List of similar characters (optional)
- **passive**: Boolean flag for passive vocabulary (default: False)
- **alternate_pronunciations**: List of alternate pronunciations (optional)
- **nohearing**: Boolean flag to disable hearing-based cards (default: False)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd anki-pleco-importer-python
```

2. Install the package:
```bash
pip install -e .
```

3. For development, install with dev dependencies:
```bash
pip install -e ".[dev]"
```

## Usage

```bash
anki-pleco-importer --help
```

## Development

### Setup

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

### Testing

Run unit tests:
```bash
pytest
```

Run BDD tests:
```bash
behave
```

Run tests with coverage:
```bash
pytest --cov=anki_pleco_importer
```

### Code Quality

Format code:
```bash
black src/ tests/
```

Type checking:
```bash
mypy src/
```

Lint code:
```bash
flake8 src/ tests/
```

## Project Structure

```
anki-pleco-importer-python/
├── src/
│   └── anki_pleco_importer/
│       ├── __init__.py
│       └── cli.py
├── features/
│   ├── steps/
│   └── *.feature
├── tests/
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── CLAUDE.md
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code quality
5. Submit a pull request

## License

MIT License