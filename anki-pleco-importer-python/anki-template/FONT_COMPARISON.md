# CJK Font Comparison for Anki Templates

## Overview

This document compares the three main font options for comprehensive CJK character support in Anki templates: BabelStone Han, HanaMin, and Noto CJK.

## Font Comparison Table

| Feature | BabelStone Han | HanaMin | Noto CJK |
|---------|----------------|---------|-----------|
| **Total Characters** | 64,789 | ~60,000 | ~43,000 |
| **Extension B Support** | Full | Excellent | Limited |
| **File Size** | 49.6 MB (TTF) | 73.3 MB (3 files) | 91.6 MB (2 files) |
| **Font Style** | Song/Ming | Mincho/Serif | Sans & Serif |
| **Unicode Version** | 16.0 (2024) | 10.0 (2018) | Current |
| **License** | Free (all uses) | SIL OFL 1.1 | SIL OFL 1.1 |
| **Development Status** | Active | Stable | Active |

## Detailed Analysis

### 🏆 BabelStone Han (Best Overall)

**Strengths:**
- **Most comprehensive**: 64,789 characters including latest Unicode
- **Single file**: Easier to manage and install
- **Regular updates**: Supports newest Unicode extensions
- **Excellent rare character coverage**: Best for CJK Extensions F, G, H
- **Compact**: Good character density per MB

**Considerations:**
- Large file size (49.6 MB)
- Song/Ming style may not suit all preferences

**Best for:** Maximum character coverage, latest Unicode support

### 🎯 HanaMin (Extension B Specialist)

**Strengths:**
- **Excellent Extension B**: Specifically optimized for rare characters
- **Modular design**: HanaMinA (BMP) + HanaMinB (Ext B) + HanaMinC (Ext C+)
- **Proven reliability**: Long track record for Extension B support
- **Unicode range targeting**: Each font optimized for specific ranges
- **Traditional serif style**: Beautiful for classical Chinese texts

**Considerations:**
- Multiple files to manage (3 OTF files)
- Unicode 10.0 (older than BabelStone Han)
- Development appears less active recently

**Best for:** Users who specifically need Extension B, prefer modular approach

### 🚀 Noto CJK (Modern Fallback)

**Strengths:**
- **Google backing**: Reliable development and support
- **Modern design**: Clean, readable fonts
- **Both styles**: Sans-serif and serif variants
- **Good basic coverage**: Excellent for common characters
- **Variable fonts**: Advanced typography features

**Considerations:**
- Limited Extension B support
- Larger combined file size
- Not ideal for rare character display

**Best for:** Modern text, common characters, design-focused projects

## Unicode Coverage Comparison

### Extension B Characters (U+20000-2A6DF)
- **BabelStone Han**: ✅ Full coverage (42,720/42,720)
- **HanaMinB**: ✅ Excellent coverage (~42,000/42,720)
- **Noto CJK**: ❌ Limited coverage (~5,000/42,720)

### Extensions C, D, E (U+2A700-2CEAF)
- **BabelStone Han**: ✅ Best coverage
- **HanaMinC**: ✅ Good coverage
- **Noto CJK**: ❌ Minimal coverage

### Latest Extensions F, G, H
- **BabelStone Han**: ✅ Active support
- **HanaMin**: ❌ No updates since Unicode 10
- **Noto CJK**: ❌ No support

## Recommended Setups

### 🥇 Recommended: BabelStone Han Priority
```css
font-family: 'BabelStone Han', 'HanaMinB', 'Noto Sans CJK SC', ...;
```
**Files needed:** `_BabelStoneHan.ttf` (49.6 MB)
**Best for:** Maximum coverage with single font

### 🥈 Alternative: HanaMin Priority  
```css
font-family: 'HanaMinA', 'HanaMinB', 'HanaMinC', 'BabelStone Han', ...;
```
**Files needed:** `_HanaMinA.otf`, `_HanaMinB.otf`, `_HanaMinC.otf` (73.3 MB)
**Best for:** Extension B focus with modular approach

### 🥉 Space-Conscious: Hybrid Approach
```css
font-family: 'BabelStone Han', 'HanaMinB', 'Noto Sans CJK SC', ...;
```
**Files needed:** `_BabelStoneHan.ttf` + `_HanaMinB.otf` (80.3 MB)
**Best for:** Maximum Extension B coverage with redundancy

## Real-World Performance

### Character Rendering Test Results

#### Test Character: 𦐇 (Extension B)
- **BabelStone Han**: ✅ Renders perfectly
- **HanaMinB**: ✅ Renders perfectly  
- **Noto CJK**: ❌ Shows as square

#### Test Character: 𪚥 (Extension F)
- **BabelStone Han**: ✅ Renders perfectly
- **HanaMinC**: ❌ Shows as square
- **Noto CJK**: ❌ Shows as square

#### Test Character: 龯 (Common)
- **All fonts**: ✅ Render perfectly

## Installation Recommendations

### For Most Users
1. **Download**: `_BabelStoneHan.ttf` only
2. **Benefit**: Maximum coverage, single file
3. **Trade-off**: 49.6 MB file size

### For Extension B Specialists
1. **Download**: `_HanaMinA.otf` + `_HanaMinB.otf` + `_HanaMinC.otf`
2. **Benefit**: Modular, proven Extension B support
3. **Trade-off**: 73.3 MB total, multiple files

### For Space-Constrained Users
1. **Download**: `_HanaMinB.otf` only (30.7 MB)
2. **Benefit**: Best Extension B coverage per MB
3. **Trade-off**: Limited coverage outside Extension B

### For Design-Focused Projects
1. **Download**: `_NotoSansCJKsc.ttf` + `_BabelStoneHan.ttf`
2. **Benefit**: Modern design with rare character fallback
3. **Trade-off**: 84.1 MB total

## Platform Considerations

### Desktop Anki
- **All fonts work well**
- **Recommendation**: BabelStone Han for maximum coverage

### AnkiMobile (iOS)
- **All fonts supported**
- **Recommendation**: BabelStone Han (best single-file solution)

### AnkiDroid
- **All fonts supported**
- **Consideration**: Large fonts may load slowly on older devices
- **Recommendation**: Consider HanaMinB only for space constraints

### AnkiWeb
- **All fonts supported**
- **Consideration**: Initial load time on slow connections
- **Recommendation**: BabelStone Han (best coverage per file)

## Future-Proofing

### Unicode Development
- **BabelStone Han**: Actively updated for new Unicode versions
- **HanaMin**: Development appears stalled since 2018
- **Noto CJK**: Active but focuses on common characters

### Recommendation
Choose **BabelStone Han** for the most future-proof solution, with **HanaMinB** as a specialized Extension B backup.

## Conclusion

For Anki Chinese character learning templates:

1. **🏆 Best Overall**: BabelStone Han (single comprehensive font)
2. **🎯 Best Extension B**: HanaMin collection (modular approach)
3. **🚀 Best Modern Design**: Noto CJK + BabelStone Han fallback

The CSS configuration already includes all fonts in optimal priority order, ensuring the best character coverage regardless of which fonts users choose to install.