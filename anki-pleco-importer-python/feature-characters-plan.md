# Feature: Character Structure Analysis

## Overview
Enhance the Anki Pleco Importer to include detailed character structure analysis, helping Chinese learners understand the compositional nature of characters through radical decomposition and component analysis.

## Problem Statement
Current Pleco exports contain character, pinyin, and definition but lack structural information that could significantly aid memorization and understanding of Chinese characters. Many learners struggle to see patterns and relationships between characters.

## Goals
- Break down characters into their fundamental components (radicals, phonetic elements)
- Provide component type classification (semantic, phonetic, positional)
- Enrich Anki cards with structural information
- Support only simplified character analysis

## User Stories
- **As a Chinese learner**, I want to see radical breakdowns of characters so I can understand their composition
- **As a Chinese learner**, I want to know which part of a character provides meaning vs. pronunciation
- **As a Chinese learner**, I want to see component relationships across multiple characters in my deck
- **As a user**, I want this analysis to be included automatically in my Anki import process

## Technical Specifications

### Core Components
1. **Character Decomposer**: Split characters into radicals/components
2. **Component Classifier**: Identify semantic vs. phonetic components
3. **OCR Integration**: Extract additional character details from screenshots
4. **Anki Field Generator**: Create structured output for Anki cards

### Data Sources
- **Unihan Database**: Unicode character decomposition data
- **CBETA Character Database**: Traditional character analysis
- **Kangxi Radical System**: 214 traditional radicals
- **Azure Computer Vision API**: OCR for screenshot analysis

### Input/Output
**Input**: 
- Pleco export files with Chinese characters
- Optional: Screenshots with character analysis

**Output**:
- Enhanced Anki CSV with additional fields:
  - `character_radicals`: List of component radicals
  - `radical_meanings`: Semantic meanings of radicals
  - `component_types`: Classification (semantic/phonetic/positional)
  - `structure_notes`: Human-readable structure explanation

## Implementation Phases

### Phase 1: Core Character Decomposition
- Integrate Unihan database for basic radical breakdown
- Create `CharacterAnalyzer` class
- Add basic radical extraction functionality
- Unit tests for character decomposition

### Phase 2: Component Classification
- Implement semantic vs. phonetic component detection
- Add positional analysis (left/right/top/bottom/enclosing)
- Create structured output formatting
- Integration with existing Pleco import pipeline

### Phase 3: OCR Integration
- Azure OCR service integration
- Screenshot processing pipeline
- Extract additional character details
- Error handling for OCR failures

### Phase 4: Anki Integration
- Extend CSV output format
- Add new Anki card fields
- Create card templates with structure visualization
- BDD tests for complete workflow

## Dependencies
- `azure-cognitiveservices-vision-computervision`: OCR functionality
- `unicodedata`: Character property access
- Character database files (Unihan, CBETA)
- Existing pandas/CSV processing pipeline

## Success Criteria
- ✅ Successfully decompose 95%+ of common Chinese characters
- ✅ Correctly classify semantic vs. phonetic components
- ✅ Generate structured Anki cards with character analysis
- ✅ Process screenshots with 90%+ OCR accuracy
- ✅ Maintain existing import performance (< 2x slowdown)
- ✅ All BDD scenarios pass for character analysis workflow

## Integration Points
- Extend `PlecoImporter` class with character analysis
- Add new CSV columns to existing output format
- Integrate with existing CLI interface
- Maintain backwards compatibility with standard imports

## Examples

### Input Character: 好 (hǎo - good)
**Decomposition Output**:
- `character_radicals`: ["女", "子"]
- `radical_meanings`: ["woman", "child"]
- `component_types`: ["semantic", "semantic"]
- `structure_notes`: "Left-right structure: woman + child = good"

### Input Character: 清 (qīng - clear)
**Decomposition Output**:
- `character_radicals`: ["氵", "青"]
- `radical_meanings`: ["water", "blue/green"]
- `component_types`: ["semantic", "phonetic"]
- `structure_notes`: "Left-right structure: water radical + 青 (phonetic component)"

## Testing Strategy
- Unit tests for each component (decomposer, classifier, OCR)
- BDD scenarios for complete user workflows
- Performance tests for large character sets
- Integration tests with existing Pleco import functionality
