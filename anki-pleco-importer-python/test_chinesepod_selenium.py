#!/usr/bin/env python3
"""
Test script for ChinesePod Selenium functionality.

Prerequisites:
1. Install Selenium: pip install selenium
2. Enable Safari WebDriver:
   - Open Safari
   - Preferences > Advanced > Check "Show Develop menu in menu bar"
   - Develop > Allow Remote Automation
   
OR install Chrome/Firefox:
   - Chrome: brew install --cask google-chrome
   - Firefox: brew install --cask firefox
"""

import logging
import sys
from src.anki_pleco_importer.chinesepod import (
    check_chinesepod_pronunciation, 
    ChinesePodSeleniumChecker,
    SELENIUM_AVAILABLE
)

def test_basic_functionality():
    """Test basic functionality without browser."""
    print("=== Basic Functionality Test ===")
    print(f"Selenium available: {SELENIUM_AVAILABLE}")
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium not available - install with: pip install selenium")
        return False
    
    print("✅ Selenium is available")
    
    # Test without browser (should fall back to requests)
    result = check_chinesepod_pronunciation('你好', use_selenium=False)
    print(f"Fallback test result: {result['available']}")
    
    return True

def test_selenium_with_browser(browser='safari'):
    """Test Selenium with actual browser."""
    print(f"\n=== Selenium Test with {browser.title()} ===")
    
    try:
        with ChinesePodSeleniumChecker(headless=False, browser=browser) as checker:
            print(f"✅ {browser.title()} WebDriver initialized successfully")
            
            # Test with a simple word
            test_words = ['你好', '学习', '中国']
            
            for word in test_words:
                print(f"\nTesting word: {word}")
                result = checker.check_pronunciation_available(word)
                
                print(f"  Available: {result['available']}")
                print(f"  URL: {result['url']}")
                print(f"  Pinyin: {result['pinyin']}")
                print(f"  Definition: {result['definition']}")
                print(f"  Audio URL: {result['audio_url']}")
                
                if result['error']:
                    print(f"  Error: {result['error']}")
                    
                # If we found any results, that's a success
                if result['available']:
                    print(f"✅ Successfully found pronunciation for {word}!")
                    return True
            
            print("ℹ️  No pronunciations found, but browser automation worked")
            return True
            
    except Exception as e:
        print(f"❌ {browser.title()} WebDriver failed: {e}")
        return False

def test_convenience_function():
    """Test the convenience function with auto-detection."""
    print("\n=== Convenience Function Test ===")
    
    test_words = ['你好', '警察']
    
    for word in test_words:
        print(f"\nTesting word: {word}")
        
        # Auto-detect best method
        result = check_chinesepod_pronunciation(word, timeout=15)
        
        print(f"  Available: {result['available']}")
        print(f"  URL: {result['url']}")
        print(f"  Method used: {'Selenium' if 'selenium' not in str(result.get('error', '')).lower() else 'Requests'}")
        
        if result['available']:
            print(f"✅ Found pronunciation for {word}!")
            print(f"  Pinyin: {result['pinyin']}")
            print(f"  Definition: {result['definition']}")

def main():
    """Run all tests."""
    logging.basicConfig(level=logging.INFO)
    
    print("ChinesePod Selenium Functionality Test")
    print("=" * 50)
    
    # Test 1: Basic functionality
    if not test_basic_functionality():
        return
    
    # Test 2: Try different browsers
    browsers_to_try = ['safari', 'chrome', 'firefox']
    
    selenium_worked = False
    for browser in browsers_to_try:
        try:
            if test_selenium_with_browser(browser):
                selenium_worked = True
                break
        except KeyboardInterrupt:
            print("\n⚠️  Browser test interrupted by user")
            break
        except Exception as e:
            print(f"❌ Failed to test {browser}: {e}")
            continue
    
    if not selenium_worked:
        print("\n⚠️  Selenium browser automation not working")
        print("Setup instructions:")
        print("1. For Safari: Enable 'Allow Remote Automation' in Safari > Develop menu")
        print("2. For Chrome: brew install --cask google-chrome")
        print("3. For Firefox: brew install --cask firefox")
    
    # Test 3: Convenience function (will fall back if needed)
    test_convenience_function()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    
    if selenium_worked:
        print("✅ Selenium-based ChinesePod checker is working!")
    else:
        print("⚠️  Selenium not fully working, but fallback to requests is available")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(1)