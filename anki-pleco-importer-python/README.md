# Anki Pleco Importer

A Python application that converts Pleco flashcard exports to Anki-compatible CSV format, specifically designed for Chinese language learning
and catering to the preferences of it's writer

## ✨ Features

### Core Functionality
- **TSV to CSV Conversion**: Transform Pleco TSV exports into Anki-importable CSV format
- **Intelligent Definition Parsing**: Extract and format complex definitions with multiple meanings
- **Pinyin Conversion**: Convert numbered pinyin (e.g., `mi2shang4`) to toned pinyin (e.g., `míshàng`)
- **Semantic Decomposition**: Automatic character breakdown with meaning explanations using hanzipy
- **Example Extraction**: Intelligently separate Chinese examples from definitions
- **HTML Formatting**: Apply rich formatting for parts of speech and domain markers
- **Anki-Ready CSV**: Generate headerless CSV files for direct Anki import

## 🚀 Installation

### Requirements
- Python 3.8+

### Install from Source
```bash
git clone <repository-url>
cd anki-pleco-importer-python
pip install -e .
```

### Development Installation
```bash
pip install -e ".[dev]"
```

## 📖 Usage

### Basic Usage
```bash
anki-pleco-importer path/to/your/pleco_export.tsv
```

This will:
1. Parse the TSV file with Chinese entries
2. Convert numbered pinyin to toned pinyin
3. Extract and format definitions with HTML markup
4. Generate semantic decomposition for characters
5. Output `processed.csv` ready for Anki import

### Example Input (TSV format)
```
迷上	mi2shang4	to become fascinated with; to become obsessed with
吟唱	yin2chang4	verb sing (a verse); chant
动弹	dong4tan5	verb move; stir 机器不动弹了。 Jīqì bù dòngtan le. The machine has stopped.
```

### Example Output (CSV format)
```
迷上,míshàng,,to become fascinated with; to become obsessed with,,,迷(mí - to bewilder/crazy about) + 上(shàng - on top/upon/above),,True,,True
吟唱,yínchàng,,<b>verb</b> sing (a verse); chant,,,吟(yín - to chant/to recite) + 唱(chàng - to sing/to call loudly),,True,,True
动弹,dòngtan,,<b>verb</b> move; stir,"机器不动弹了。 Jīqì bù dòngtan le. The machine has stopped.",,"动(dòng - to move/to set in movement) + 弹(dàn - bullet/shot/to spring)",,True,,True
```

## 🏗️ Architecture

### AnkiCard Model
The application uses a comprehensive `AnkiCard` model:

```python
@dataclass
class AnkiCard:
    pinyin: str                           # Toned pinyin (míshàng)
    simplified: str                       # Chinese characters (迷上)
    pronunciation: Optional[str] = None   # Audio file, you have to add this yourself
    meaning: str = ""                     # Formatted definition with HTML
    examples: Optional[List[str]] = None  # Chinese examples with translations
    phonetic_component: Optional[str] = None # used only for single characters
    structural_decomposition: Optional[str] = None  # Character decomposition
    similar_characters: Optional[List[str]] = None
    passive: bool = False                 # Default: True in conversion
    alternate_pronunciations: Optional[List[str]] = None
    nohearing: bool = False              # Default: True in conversion
```

## 🧪 Testing

### Run Tests
```bash
# Unit tests
pytest

# BDD tests
behave

# All tests with coverage
pytest --cov=anki_pleco_importer
```

## 🛠️ Development

### Code Quality Tools
```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Lint code
flake8 src/ tests/
```

### Project Structure
```
anki-pleco-importer-python/
├── src/anki_pleco_importer/
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── pleco.py            # Pleco data models and parsing
│   ├── anki.py             # Anki card models
│   ├── chinese.py          # Chinese text processing
│   └── constants.py        # Configuration and regex patterns
├── features/
│   ├── pleco_conversion.feature  # BDD scenarios
│   ├── cli_interface.feature
│   ├── steps/
│   │   ├── conversion_steps.py
│   │   └── cli_steps.py
│   └── examples/
│       └── import.tsv
├── tests/
│   └── test_pinyin_conversion.py
├── pyproject.toml
├── CLAUDE.md               # Project instructions
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the existing patterns
4. Ensure all tests pass (`pytest && behave`)
5. Run code quality checks (`black`, `mypy`, `flake8`)
6. Submit a pull request

### Development Guidelines
- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation as needed
- Use descriptive commit messages

## 📝 License

MIT License - see LICENSE file for details.

## 🔧 Troubleshooting

### Common Issues
- **Import Errors**: Ensure all dependencies are installed (`pip install -e ".[dev]"`)
- **Character Encoding**: Make sure TSV files are UTF-8 encoded
- **Empty Output**: Check that input TSV has correct format (Chinese\tpinyin\tdefinition)

### Debug Mode
Use `--help` to see all available options:
```bash
anki-pleco-importer --help
```
