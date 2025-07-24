# Auto-Rotating Anki Themes

This system automatically rotates between different Anki card themes based on the current date, providing a fresh visual experience every day while maintaining consistency throughout each study session.

## 🎯 Features

- **Daily Theme Rotation**: Themes change automatically every day
- **4 Beautiful Themes**: Original Default, Zen Vertical, Zen Default Hybrid, and Neon Cyberpunk
- **Consistent Daily Experience**: Same theme for entire day across all sessions
- **Smooth Transitions**: CSS transitions for seamless theme changes
- **Mobile Responsive**: All themes adapt to different screen sizes
- **Manual Override**: Test specific themes for customization
- **Easy Expansion**: Add new themes easily

## 📅 Theme Rotation Schedule

The system uses a 4-theme cycle based on day of year:

| Theme | Days |
|-------|------|
| **Original Default** | 1, 5, 9, 13, 17, 21, 25... |
| **Zen Vertical** | 2, 6, 10, 14, 18, 22, 26... |
| **Zen Default Hybrid** | 3, 7, 11, 15, 19, 23, 27... |
| **Neon Cyberpunk** | 4, 8, 12, 16, 20, 24, 28... |

## 🚀 Quick Setup

### 1. Copy Files to Anki
Copy these files to your Anki media folder:
- `auto-rotating-themes.css`
- `theme-rotator.js`

**Anki Media Folder Locations:**
- **Windows**: `%APPDATA%\Anki2\[Profile]\collection.media\`
- **macOS**: `~/Library/Application Support/Anki2/[Profile]/collection.media/`
- **Linux**: `~/.local/share/Anki2/[Profile]/collection.media/`

### 2. Update Card Templates

Replace your existing card templates with:

**Front Template:**
```html
{{#Chinese}}
<div class="card-container">
  <div class="chinese-header">
    <div class="chinese-main">{{Chinese}}</div>
    <div class="chinese-side">
      {{#Pinyin}}<div class="pinyin-main">{{Pinyin}}</div>{{/Pinyin}}
      {{#Audio}}<div class="audio-section">{{Audio}}</div>{{/Audio}}
    </div>
  </div>
  <div class="prompt">Think of the meaning...</div>
</div>

<!-- Auto-Rotating Theme System -->
<link rel="stylesheet" type="text/css" href="auto-rotating-themes.css">
<script src="theme-rotator.js"></script>
{{/Chinese}}
```

**Back Template:**
```html
{{#Simplified}}
<div class="card-container">
  <!-- Front repeated for context -->
  <div class="chinese-header">
    <div class="chinese-main">{{Simplified}}</div>
    <div class="chinese-side">
      {{#Pinyin}}<div class="pinyin-main">{{Pinyin}} {{Pronunciation}}</div>{{/Pinyin}}
    </div>
  </div>

  <hr class="divider">

  <!-- Back content -->
  {{#Definition}}
  <div class="definition-section">
    <div class="section-title">Definition</div>
    <div class="definition-content">{{Definition}}</div>
  </div>
  {{/Definition}}

  {{#Components}}
  <div class="components-section">
    <div class="section-title">Structural Analysis</div>
    <div class="components-content">{{Components}}</div>
  </div>
  {{/Components}}

  {{#Examples}}
  <div class="examples-section">
    <div class="section-title">Examples</div>
    <div class="examples-content">{{Examples}}</div>
  </div>
  {{/Examples}}

  {{#SimilarChars}}
  <div class="similar-section">
    <div class="section-title">Similar Characters</div>
    <div class="similar-content">{{SimilarChars}}</div>
  </div>
  {{/SimilarChars}}
</div>

<!-- Auto-Rotating Theme System -->
<link rel="stylesheet" type="text/css" href="auto-rotating-themes.css">
<script src="theme-rotator.js"></script>
{{/Simplified}}
```

### 3. Set Card Styling (Optional)
You can use `styling-with-rotation.css` as your card styling for fallback support, or leave the styling section empty since themes are loaded dynamically.

## 🧪 Testing & Debugging

### Browser Console Commands
Open browser console (F12) and use these commands:

```javascript
// Check current theme info
ankiThemeInfo

// Manually set a specific theme
setAnkiTheme('zen-vertical')
setAnkiTheme('neon-cyberpunk')
setAnkiTheme('original-default')
setAnkiTheme('zen-default-hybrid')

// Reset to automatic theme
location.reload()
```

### Preview System
Open `auto-rotation-preview.html` in your browser to:
- See all themes in action
- Test theme switching
- Understand the rotation schedule
- Check mobile responsiveness

## 🎨 Available Themes

### 1. Original Default
- Clean, functional design
- Horizontal layout
- Modern sans-serif fonts
- Blue accent colors

### 2. Zen Vertical
- Traditional scroll-inspired design
- Vertical text orientation for Chinese
- Minimalist aesthetics
- Subtle gradients and shadows

### 3. Zen Default Hybrid
- Combines horizontal layout with traditional fonts
- Elegant typography
- Clean and balanced
- Best of both worlds

### 4. Neon Cyberpunk
- Futuristic terminal design
- Neon glow effects
- Dark theme with bright accents
- Monospace fonts

## ⚙️ Customization

### Adding New Themes

1. **Add CSS to `auto-rotating-themes.css`:**
```css
.theme-yourtheme .card {
  /* Your theme styles */
}
/* Add all necessary selectors with .theme-yourtheme prefix */
```

2. **Update `theme-rotator.js`:**
```javascript
const THEMES = [
    'original-default',
    'zen-vertical',
    'zen-default-hybrid',
    'neon-cyberpunk',
    'yourtheme'  // Add your theme here
];
```

### Configuration Options

Edit `theme-rotator.js` to customize:

```javascript
const CONFIG = {
    // Enable theme persistence across sessions
    persistTheme: true,

    // Show debug info in console
    debugMode: false,

    // Transition duration in milliseconds
    transitionDuration: 300
};
```

### Changing Rotation Schedule

Modify the `THEMES` array in `theme-rotator.js`:
- **2 themes**: Changes every 2 days
- **3 themes**: Changes every 3 days
- **4 themes**: Changes every 4 days (current)
- **7 themes**: Changes weekly

## 🔧 Troubleshooting

### Themes Not Loading
1. Verify files are in correct Anki media folder
2. Check browser console for JavaScript errors
3. Ensure file names match exactly (case-sensitive)
4. Restart Anki and sync

### Theme Stuck on One Style
1. Clear browser cache
2. Check console with `ankiThemeInfo`
3. Manually reset with `location.reload()`

### Mobile Issues
- All themes are responsive
- Test on different screen sizes
- Some themes (like Zen Vertical) have mobile-optimized layouts

## 📱 Platform Compatibility

- ✅ **Anki Desktop** (Windows, macOS, Linux)
- ✅ **AnkiWeb** (Browser-based)
- ✅ **AnkiMobile** (iOS) - with some limitations
- ⚠️ **AnkiDroid** (Android) - may need adjustments

## 🔄 Updates & Maintenance

The system is self-contained and requires no maintenance. Themes will continue rotating automatically based on the system date.

To update:
1. Replace the CSS/JS files with new versions
2. Themes and rotation logic are preserved
3. No need to modify card templates

## 📄 File Structure

```
anki-template/
├── auto-rotating-themes.css          # Master CSS with all themes
├── theme-rotator.js                  # JavaScript rotation logic
├── front-template-with-rotation.html # Updated front template
├── back-template-with-rotation.html  # Updated back template
├── styling-with-rotation.css         # Base/fallback styles
├── auto-rotation-preview.html        # Preview and testing
└── README-auto-rotation.md           # This documentation
```

## 💡 Tips

1. **Preview First**: Use `auto-rotation-preview.html` to test before implementing
2. **Backup Templates**: Save your current templates before switching
3. **Gradual Rollout**: Test on a small deck first
4. **Theme Consistency**: Each theme maintains the same information hierarchy
5. **Performance**: Themes load instantly with CSS classes, no performance impact

Enjoy your auto-rotating Anki themes! 🎨✨
