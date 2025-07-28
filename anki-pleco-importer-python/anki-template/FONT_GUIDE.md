# Font Setup Guide for Anki CJK Character Support

## Overview
This guide shows how to include comprehensive CJK fonts directly in your Anki collection to ensure proper rendering of rare Chinese characters and components across all devices and platforms.

## Why Include Fonts in Anki Collection?
- **Offline Access**: Fonts work without internet connection
- **Cross-Platform**: Works on desktop, mobile, and AnkiWeb
- **No System Dependencies**: No need to install fonts on each device
- **Consistent Rendering**: Same appearance across all platforms
- **Sync Compatibility**: Fonts sync with your collection automatically

## Required Font Files

### 1. BabelStone Han (Primary - Best Coverage)
**Download from**: https://www.babelstone.co.uk/Fonts/Han.html

Required files:
- `BabelStoneHan.woff2` (recommended, smallest size ~19MB)
- `BabelStoneHan.woff` (fallback, ~25MB)
- `BabelStoneHan.ttf` (final fallback, ~49MB)

**Coverage**: 60,000+ characters including CJK Extensions A-H

### 2. HanaMin Fonts (Alternative Comprehensive)
**Download from**: https://github.com/cjkvi/HanaMinAFDKO/releases

Required files:
- `HanaMinA.otf` (30.2 MB) - Basic Multilingual Plane
- `HanaMinB.otf` (30.7 MB) - CJK Extension B (rare characters)
- `HanaMinC.otf` (12.4 MB) - Extensions C+ coverage

**Coverage**: Excellent Extension B support, Unicode 10 compatible

### 3. Noto CJK Fonts (Alternative/Supplement)
**Download from**: https://fonts.google.com/noto

Required files:
- `NotoSansCJKsc-Regular.woff2`
- `NotoSerifCJKsc-Regular.woff2`

**Coverage**: Good modern CJK support, limited rare character coverage

## Installation Instructions

### Step 1: Download Font Files
1. Download BabelStone Han from the official website
2. Optionally download Noto CJK fonts for additional coverage

### Step 2: Rename Font Files for Anki
Rename files with underscore prefix (Anki requirement for media files):
```
BabelStoneHan.woff2 → _BabelStoneHan.woff2
BabelStoneHan.woff → _BabelStoneHan.woff
BabelStoneHan.ttf → _BabelStoneHan.ttf
HanaMinA.otf → _HanaMinA.otf
HanaMinB.otf → _HanaMinB.otf
HanaMinC.otf → _HanaMinC.otf
NotoSansCJKsc-Regular.woff2 → _NotoSansCJKsc.woff2
NotoSerifCJKsc-Regular.woff2 → _NotoSerifCJKsc.woff2
```

### Step 3: Add Fonts to Anki Collection

#### Method 1: Direct Copy (Recommended)
1. Find your Anki media folder:
   - **Windows**: `%APPDATA%\Anki2\[Profile]\collection.media\`
   - **macOS**: `~/Library/Application Support/Anki2/[Profile]/collection.media/`
   - **Linux**: `~/.local/share/Anki2/[Profile]/collection.media/`

2. Copy renamed font files to this folder

#### Method 2: Import via Anki
1. Open Anki
2. Create a temporary note
3. Edit the note and use "Attach" button to add each font file
4. Anki will automatically rename and import the files
5. Delete the temporary note (fonts remain in collection)

#### Method 3: Field Import
1. Add font files as attachments to any existing note
2. Reference them in card templates using `_filename` format

### Step 4: Verify Installation
1. Check that font files appear in your media folder with `_` prefix
2. Sync your collection to upload fonts to AnkiWeb
3. Test on different devices to ensure fonts load correctly

## File Size Considerations

### Recommended Setup (Best Balance)
```
_BabelStoneHan.woff2     (~19MB) - Primary comprehensive font
_HanaMinB.otf            (~31MB) - Extension B specialist
Total: ~50MB
```

### HanaMin Alternative (Excellent Extension B)
```
_HanaMinA.otf            (~30MB) - BMP coverage
_HanaMinB.otf            (~31MB) - Extension B coverage  
_HanaMinC.otf            (~12MB) - Extensions C+ coverage
Total: ~73MB
```

### Minimal Setup (Space Constrained)
```
_BabelStoneHan.woff2     (~19MB) - Only the essential font
OR
_HanaMinB.otf            (~31MB) - Extension B focus
Total: ~19-31MB
```

### Complete Setup (Maximum Coverage)
```
_BabelStoneHan.ttf       (~49MB)
_HanaMinA.otf            (~30MB)
_HanaMinB.otf            (~31MB)
_HanaMinC.otf            (~12MB)
_NotoSansCJKsc.ttf       (~35MB)
_NotoSerifCJKsc.ttf      (~57MB)
Total: ~214MB
```

## Sync Considerations

### Initial Sync
- First sync after adding fonts will take longer due to file size
- Ensure stable internet connection for upload
- Consider syncing on Wi-Fi for mobile devices

### Ongoing Syncs
- Fonts only upload once, subsequent syncs are normal speed
- Font files persist across device installations
- Backup includes fonts automatically

## Platform-Specific Notes

### AnkiDroid
- Supports custom fonts via media collection
- May take longer to load large fonts initially
- Consider using WOFF2 format for smaller size

### AnkiMobile (iOS)
- Full support for collection-embedded fonts
- No additional configuration needed
- Fonts work offline immediately

### Desktop Anki
- Fastest loading of embedded fonts
- Supports all font formats
- Best performance with WOFF2

### AnkiWeb
- Full support for embedded fonts
- May have slower initial load for large fonts
- Works across all browsers

## Troubleshooting

### Fonts Not Loading
1. **Check file names**: Must start with `_` (underscore)
2. **Verify sync**: Ensure fonts uploaded to AnkiWeb
3. **Clear cache**: Try Tools > Check Database in Anki
4. **Check file size**: Very large fonts may time out on slow connections

### Characters Still Show as Squares
1. **Font order**: BabelStone Han should be first in CSS
2. **Unicode range**: Verify character is in supported range
3. **Font corruption**: Re-download and re-import font files
4. **Device limitations**: Some very old devices may not support large fonts

### Sync Issues
1. **Upload timeout**: Split large fonts across multiple sync sessions
2. **Storage limits**: Check AnkiWeb storage quota
3. **Connection issues**: Use stable Wi-Fi for initial font upload

## CSS Integration

The templates are already configured to use these fonts. The CSS automatically:
1. Tries BabelStone Han first for rare characters
2. Falls back to Noto CJK fonts
3. Uses system fonts as final fallback
4. Applies fonts specifically to component analysis

## Font Stack Priority
```css
font-family: 'BabelStone Han', 'HanaMinA', 'HanaMinB', 'HanaMinC',
             'Noto Sans CJK SC', 'Noto Serif CJK SC', 
             'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 
             'SimSun-ExtB', 'MingLiU-ExtB', sans-serif;
```

## Testing Your Setup

### Test Characters
Use these characters to verify font coverage:
- Common: 汉字学习 (should work with any font)
- Extension A: 㐀㐁㐂 (tests Extension A coverage)
- Extension B: 𠀀𠀁𦐇 (tests rare character support)
- Components: ⻊⻌⻍ (tests component radicals)

### Verification Steps
1. Create a test note with rare characters
2. Check display on desktop Anki
3. Sync and verify on mobile devices
4. Test offline functionality

## License Information

### BabelStone Han
- **License**: Free for personal and commercial use
- **Credit**: Created by Andrew West
- **Website**: https://www.babelstone.co.uk/

### HanaMin
- **License**: SIL Open Font License 1.1
- **Credit**: CJKVI Group, kawabata
- **Website**: https://github.com/cjkvi/HanaMinAFDKO

### Noto CJK
- **License**: SIL Open Font License 1.1
- **Credit**: Google Fonts
- **Website**: https://fonts.google.com/noto

All fonts can be legally embedded in Anki collections and distributed.