# Anki Template Setup Guide

## Quick Setup Steps

### 1. Create Note Type in Anki
1. Open Anki
2. Go to **Tools** → **Manage Note Types**
3. Click **Add** → **Add: Basic**
4. Name it "Chinese Learning"

### 2. Configure Fields
Click **Fields...** and add these fields in order:
1. `Chinese`
2. `Pinyin`
3. `Audio`
4. `Definition`
5. `Examples`
6. `SimilarChars`
7. `Components`
8. `AlternatePron`
9. `Passive`
10. `NohearingFlag`

### 3. Set Up Templates
Click **Cards...** then:

**Front Template**: Copy content from `front-template.html`
**Back Template**: Copy content from `back-template.html`
**Styling**: Copy content from `styling.css`

### 4. Import Data
1. Generate CSV with: `python -m anki_pleco_importer.cli convert your_file.tsv`
2. In Anki: **File** → **Import**
3. Select your CSV file
4. Map fields to match the note type
5. Import

## Field Mapping for CSV Import

When importing, map CSV columns to these Anki fields:
- Column 1 → Chinese
- Column 2 → Pinyin
- Column 3 → Audio
- Column 4 → Definition
- Column 5 → Examples
- Column 6 → SimilarChars
- Column 7 → Components
- Column 8 → AlternatePron
- Column 9 → Passive
- Column 10 → NohearingFlag

## Features

✅ **Mobile Optimized**: Perfect for studying on phones
✅ **Clean Design**: Focuses attention on learning
✅ **Semantic HTML**: Proper structure for accessibility
✅ **Dark Mode**: Automatically adapts to system preference
✅ **Progressive Disclosure**: Shows information when you need it
✅ **Color Coded**: Parts of speech, domains, and usage markers are visually distinct
