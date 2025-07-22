/*
 * Anki Theme Auto-Rotator
 * Automatically rotates between different card themes based on the current date
 *
 * How it works:
 * 1. Calculates current day of year
 * 2. Uses modulo to cycle through available themes
 * 3. Applies appropriate theme class to the card
 * 4. Provides consistent theming for the entire day
 */

(function() {
    'use strict';

    // Available themes - add/remove themes here to change rotation
    const THEMES = [
        'original-default',
        'zen-vertical',
        'zen-default-hybrid',
        'neon-cyberpunk'
    ];

    // Configuration
    const CONFIG = {
        // Set to true to enable theme persistence across browser sessions
        // (theme will be the same for the entire day regardless of page refreshes)
        persistTheme: true,

        // Set to true to show current theme info in console
        debugMode: false,

        // Theme transition effect duration (in ms)
        transitionDuration: 300
    };

    /**
     * Calculate current day of year (1-365/366)
     * @returns {number} Day of year
     */
    function getCurrentDayOfYear() {
        const now = new Date();
        const start = new Date(now.getFullYear(), 0, 1);
        const diff = now - start;
        const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24)) + 1;
        return dayOfYear;
    }

    /**
     * Get theme for current date
     * @returns {string} Theme name
     */
    function getCurrentTheme() {
        const dayOfYear = getCurrentDayOfYear();
        const themeIndex = (dayOfYear - 1) % THEMES.length;
        return THEMES[themeIndex];
    }

    /**
     * Get cached theme from sessionStorage if available
     * @returns {string|null} Cached theme or null
     */
    function getCachedTheme() {
        if (!CONFIG.persistTheme) return null;

        try {
            const cached = sessionStorage.getItem('anki-theme-cache');
            if (!cached) return null;

            const { theme, date } = JSON.parse(cached);
            const today = new Date().toDateString();

            // Return cached theme if it's for today
            return date === today ? theme : null;
        } catch (e) {
            // Clear invalid cache
            sessionStorage.removeItem('anki-theme-cache');
            return null;
        }
    }

    /**
     * Cache current theme for the day
     * @param {string} theme Theme to cache
     */
    function cacheTheme(theme) {
        if (!CONFIG.persistTheme) return;

        try {
            const cacheData = {
                theme: theme,
                date: new Date().toDateString()
            };
            sessionStorage.setItem('anki-theme-cache', JSON.stringify(cacheData));
        } catch (e) {
            // Storage might be full or disabled, continue without caching
            if (CONFIG.debugMode) {
                console.warn('Unable to cache theme:', e);
            }
        }
    }

    /**
     * Apply theme to the document
     * @param {string} theme Theme name to apply
     */
    function applyTheme(theme) {
        const body = document.body;

        // Remove any existing theme classes
        THEMES.forEach(t => body.classList.remove(`theme-${t}`));

        // Add the current theme class
        body.classList.add(`theme-${theme}`);

        // Add transition class for smooth theme changes
        body.style.transition = `all ${CONFIG.transitionDuration}ms ease-in-out`;

        // Cache the theme
        cacheTheme(theme);

        if (CONFIG.debugMode) {
            console.log(`Applied theme: ${theme} (day ${getCurrentDayOfYear()})`);
        }
    }

    /**
     * Get theme info for debugging
     * @returns {object} Theme information
     */
    function getThemeInfo() {
        const dayOfYear = getCurrentDayOfYear();
        const currentTheme = getCurrentTheme();
        const themeIndex = THEMES.indexOf(currentTheme);

        return {
            dayOfYear,
            currentTheme,
            themeIndex,
            totalThemes: THEMES.length,
            availableThemes: THEMES,
            nextTheme: THEMES[(themeIndex + 1) % THEMES.length],
            daysUntilNextTheme: THEMES.length - ((dayOfYear - 1) % THEMES.length)
        };
    }

    /**
     * Initialize theme rotation system
     */
    function init() {
        // Try to get cached theme first
        let currentTheme = getCachedTheme();

        // If no cached theme, calculate current theme
        if (!currentTheme) {
            currentTheme = getCurrentTheme();
        }

        // Apply the theme
        applyTheme(currentTheme);

        // Debug information
        if (CONFIG.debugMode) {
            const info = getThemeInfo();
            console.group('🎨 Anki Theme Rotator');
            console.log('Current theme:', info.currentTheme);
            console.log('Day of year:', info.dayOfYear);
            console.log('Theme index:', info.themeIndex + 1, 'of', info.totalThemes);
            console.log('Next theme:', info.nextTheme, 'in', info.daysUntilNextTheme, 'days');
            console.log('All themes:', info.availableThemes);
            console.groupEnd();
        }

        // Expose theme info to global scope for manual inspection
        window.ankiThemeInfo = getThemeInfo();
    }

    /**
     * Manual theme override function (useful for testing)
     * @param {string} themeName Theme name to apply
     */
    function setTheme(themeName) {
        if (!THEMES.includes(themeName)) {
            console.error(`Theme "${themeName}" not found. Available themes:`, THEMES);
            return false;
        }

        applyTheme(themeName);
        console.log(`Manually set theme to: ${themeName}`);
        return true;
    }

    // Expose manual theme setter to global scope
    window.setAnkiTheme = setTheme;

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM is already loaded
        init();
    }

    // Re-check theme on focus (in case date changed while tab was inactive)
    window.addEventListener('focus', function() {
        const cachedTheme = getCachedTheme();
        const currentTheme = getCurrentTheme();

        // If cached theme doesn't match current theme, update
        if (!cachedTheme || cachedTheme !== currentTheme) {
            applyTheme(currentTheme);
        }
    });

})();

/*
 * Usage Instructions:
 *
 * 1. Include this script in your Anki card template
 * 2. Make sure auto-rotating-themes.css is also included
 * 3. The script will automatically apply themes based on the current date
 *
 * Manual theme testing:
 * - Open browser console
 * - Type: setAnkiTheme('zen-vertical') to test a specific theme
 * - Type: ankiThemeInfo to see current theme information
 *
 * Adding new themes:
 * 1. Add your theme CSS with .theme-yourname prefix to auto-rotating-themes.css
 * 2. Add 'yourname' to the THEMES array above
 *
 * Theme rotation schedule (4 themes):
 * - Day 1, 5, 9, 13... : original-default
 * - Day 2, 6, 10, 14... : zen-vertical
 * - Day 3, 7, 11, 15... : zen-default-hybrid
 * - Day 4, 8, 12, 16... : neon-cyberpunk
 */
