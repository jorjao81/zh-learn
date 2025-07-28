# Anki Templates for Chinese Character Learning

This directory contains Anki card templates optimized for Chinese character learning with comprehensive CJK font support for rare characters and components.

## Quick Start

### 1. Download Fonts (One-time setup)
```bash
python download_fonts.py
```

### 2. Install Fonts to Anki
```bash
python install_fonts.py
```

### 3. Import Templates
Copy the CSS and HTML templates to your Anki card types.

## Features

### ✨ Comprehensive Character Support
- **BabelStone Han**: 60,000+ characters including CJK Extensions A-H
- **Noto CJK**: Modern fallback fonts for additional coverage
- **Rare Components**: Proper rendering of characters like 𦐇, ⻊, etc.

### 🎨 Multiple Themes
- `styling.css` - Default clean theme
- `themes/modern-minimalist.css` - Modern sans-serif style  
- `themes/traditional-brush.css` - Classical calligraphy style
- `themes/zen-default-hybrid.css` - Zen-inspired layout
- And 6 more creative themes

### 📱 Cross-Platform Compatibility
- Works on Anki Desktop (Windows, macOS, Linux)
- AnkiMobile (iOS) with full font support
- AnkiDroid with embedded font loading
- AnkiWeb with browser compatibility

## Font Architecture

### Font Stack Priority
```css
font-family: 'BabelStone Han', 'Noto Sans CJK SC', 'Noto Serif CJK SC', 
             'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 
             'SimSun-ExtB', 'MingLiU-ExtB', sans-serif;
```

### Local Font Loading
Fonts are embedded in your Anki collection as `_FontName.ttf` files:
- `_BabelStoneHan.ttf` (49.6 MB) - Primary comprehensive font
- `_NotoSansCJKsc.ttf` (34.5 MB) - Modern sans-serif fallback
- `_NotoSerifCJKsc.ttf` (57.1 MB) - Serif style alternative

### CSS Variables
```css
:root {
  --cjk-font-stack: 'BabelStone Han', 'Noto Sans CJK SC', ...;
  --cjk-serif-stack: 'BabelStone Han', 'Noto Serif CJK SC', ...;
}
```

## File Structure

```
anki-template/
├── README_FONTS.md                # This file
├── FONT_GUIDE.md                  # Detailed font setup guide
├── download_fonts.py              # Download script for fonts
├── install_fonts.py               # Install fonts to Anki
├── styling.css                    # Main theme CSS
├── themes/
│   ├── cjk-fonts.css             # Shared font declarations
│   ├── modern-minimalist.css     # Clean modern theme
│   ├── traditional-brush.css     # Classical theme
│   ├── zen-default-hybrid.css    # Zen-inspired theme
│   ├── elegant-gradient.css      # Gradient backgrounds
│   ├── neon-cyberpunk.css        # Futuristic theme
│   ├── paper-notebook.css        # Notebook-style theme
│   ├── high-contrast-dark.css    # High contrast dark mode
│   ├── classic-academic.css      # Academic journal style
│   └── ancient-scroll.css        # Traditional scroll theme
├── fonts/
│   ├── README.md                 # Font installation guide
│   ├── _BabelStoneHan.ttf        # Primary CJK font
│   ├── _NotoSansCJKsc.ttf        # Sans-serif fallback
│   └── _NotoSerifCJKsc.ttf       # Serif fallback
└── previews/                     # Theme preview images
    ├── single-character-previews.html
    ├── tree-structure-preview.html
    └── ...
```

## Usage Instructions

### Step 1: Font Setup
1. Run `python download_fonts.py` to download required fonts
2. Run `python install_fonts.py` to copy fonts to your Anki media folder
3. Sync your Anki collection to upload fonts to AnkiWeb

### Step 2: Template Integration
1. Open Anki and go to Browse
2. Select a Chinese character note
3. Click "Cards..." to edit the card template
4. Copy the CSS from `styling.css` to the "Styling" section
5. Update your card templates to use the semantic markup classes

### Step 3: Theme Customization
To use a different theme:
1. Replace the `@import url('themes/cjk-fonts.css');` line with your chosen theme
2. Or combine multiple theme files for custom styling

## Semantic Markup Classes

The templates use semantic HTML classes for proper styling:

### Character Components
```html
<span class="hanzi">字</span>           <!-- Chinese characters -->
<span class="pinyin">zì</span>         <!-- Pinyin pronunciation -->
<span class="translation">character</span> <!-- English translation -->
```

### Component Analysis
```html
<span class="semantic">土</span>        <!-- Semantic component -->
<span class="phonetic">也</span>        <!-- Phonetic component -->
<span class="unknown">弋</span>         <!-- Unknown component type -->
```

### Part of Speech & Domain Tags
```html
<span class="part-of-speech">noun</span>    <!-- POS tags -->
<span class="domain">medicine</span>        <!-- Domain markers -->
<span class="usage literary">literary</span> <!-- Usage markers -->
```

## Testing Your Setup

### Verification Characters
Test these characters to ensure fonts are working:
- **Common**: 汉字学习 (should work with any font)
- **Extension A**: 㐀㐁㐂 (tests Extension A coverage)  
- **Extension B**: 𠀀𠀁𦐇 (tests rare character support)
- **Components**: ⻊⻌⻍ (tests component radicals)

### Troubleshooting
1. **Characters show as squares**: Install BabelStone Han font
2. **Fonts not loading**: Check file names start with `_` underscore
3. **Sync issues**: Use stable Wi-Fi for initial font upload
4. **Performance issues**: Large fonts may load slowly on mobile

## Font Licenses

### BabelStone Han
- **License**: Free for personal and commercial use
- **Author**: Andrew West
- **Website**: https://www.babelstone.co.uk/

### Noto CJK
- **License**: SIL Open Font License 1.1  
- **Author**: Google Fonts
- **Website**: https://fonts.google.com/noto

Both fonts can be legally embedded in Anki collections and distributed.

## Technical Specifications

### Unicode Coverage
- **U+4E00-9FFF**: CJK Unified Ideographs (20,992 characters)
- **U+3400-4DBF**: CJK Extension A (6,592 characters)
- **U+20000-2A6DF**: CJK Extension B (42,720 characters)
- **U+2A700-2B73F**: CJK Extension C (4,160 characters)
- **U+2B740-2B81F**: CJK Extension D (224 characters)
- **U+2B820-2CEAF**: CJK Extension E (5,776 characters)

### Browser Support
- Chrome/Chromium: Full support
- Firefox: Full support  
- Safari: Full support
- Edge: Full support
- Mobile browsers: Varies by device

### Performance Optimization
- Font files use `font-display: swap` for faster loading
- Unicode-range declarations optimize font loading
- WOFF2 format prioritized for smaller file sizes
- Fallback fonts ensure graceful degradation

## Contributing

When adding new themes or features:
1. Include the `@import url('themes/cjk-fonts.css');` for font support
2. Test with rare characters to ensure proper rendering
3. Maintain semantic markup compatibility
4. Test across desktop and mobile platforms

## Support

For font-related issues:
1. Check the [FONT_GUIDE.md](FONT_GUIDE.md) for detailed troubleshooting
2. Verify font installation with the test characters above
3. Ensure your Anki collection has synced successfully
4. Test on multiple devices to isolate platform-specific issues