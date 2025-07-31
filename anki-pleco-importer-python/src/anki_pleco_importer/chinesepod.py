"""ChinesePod dictionary checker for Chinese word pronunciations using Selenium."""

import logging
import re
import time
from typing import Optional, Dict, Any, List
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup

# Selenium imports - optional dependency
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

logger = logging.getLogger(__name__)


class ChinesePodError(Exception):
    """Base exception for ChinesePod-related errors."""

    pass


class ChinesePodSeleniumChecker:
    """Selenium-based ChinesePod dictionary pronunciation checker."""

    def __init__(self, headless: bool = True, timeout: int = 10, browser: str = "safari"):
        """Initialize the Selenium-based ChinesePod checker.

        Args:
            headless: Run browser in headless mode (not supported for Safari)
            timeout: Default timeout for operations in seconds
            browser: Browser to use ("chrome", "firefox", or "safari")
        """
        if not SELENIUM_AVAILABLE:
            raise ChinesePodError("Selenium is not installed. Run: pip install selenium")

        self.headless = headless
        self.timeout = timeout
        self.browser = browser.lower()
        self.driver = None
        self.base_url = "https://www.chinesepod.com/dictionary"

    def __enter__(self):
        """Context manager entry."""
        self._init_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def _init_driver(self):
        """Initialize the WebDriver."""
        try:
            if self.browser == "chrome":
                options = ChromeOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
                self.driver = webdriver.Chrome(options=options)
            elif self.browser == "firefox":
                options = FirefoxOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.set_preference(
                    "general.useragent.override",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Gecko/20100101 Firefox/91.0",
                )
                self.driver = webdriver.Firefox(options=options)
            elif self.browser == "safari":
                # Safari WebDriver doesn't support headless mode
                if self.headless:
                    logger.warning("Safari WebDriver doesn't support headless mode, running in normal mode")
                self.driver = webdriver.Safari()
            else:
                raise ChinesePodError(f"Unsupported browser: {self.browser}")

            self.driver.set_page_load_timeout(self.timeout)
            self.driver.implicitly_wait(5)

        except WebDriverException as e:
            raise ChinesePodError(f"Failed to initialize {self.browser} WebDriver: {e}")

    def close(self):
        """Close the WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

    def check_pronunciation_available(self, word: str) -> Dict[str, Any]:
        """Check if pronunciation is available for a Chinese word using Selenium.

        Args:
            word: Chinese word to check

        Returns:
            Dictionary containing:
            - available: bool - whether pronunciation is available
            - url: str - the URL that was checked
            - pinyin: str or None - pinyin if found
            - audio_url: str or None - direct audio URL if found
            - definition: str or None - English definition if found
            - error: str or None - error message if failed
        """
        result = {
            "available": False,
            "url": self.base_url,
            "pinyin": None,
            "audio_url": None,
            "definition": None,
            "error": None,
        }

        if not self.driver:
            self._init_driver()

        try:
            logger.info(f"Searching ChinesePod for word: {word}")

            # Navigate to dictionary page
            self.driver.get(self.base_url)

            # Wait for page to load
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Look for search input field
            search_selectors = [
                'input[type="search"]',
                'input[placeholder*="search"]',
                'input[placeholder*="Search"]',
                "#search",
                ".search-input",
                'input[name="search"]',
                'input[name="query"]',
                'input[name="q"]',
            ]

            search_input = None
            for selector in search_selectors:
                try:
                    search_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if search_input.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if not search_input:
                # Try looking for any input field
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    if inp.is_displayed() and inp.get_attribute("type") not in ["hidden", "submit", "button"]:
                        search_input = inp
                        break

            if not search_input:
                result["error"] = "Could not find search input field on ChinesePod dictionary page"
                return result

            logger.debug(f"Found search input: {search_input.tag_name} with id='{search_input.get_attribute('id')}'")

            # Clear and enter the search term
            search_input.clear()
            search_input.send_keys(word)

            # Look for search button or submit
            search_button = None
            button_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                "button.search",
                ".search-button",
                "button",
                'input[value*="Search"]',
                'input[value*="search"]',
            ]

            for selector in button_selectors:
                try:
                    search_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if search_button.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if search_button:
                search_button.click()
                logger.debug("Clicked search button")
            else:
                # Try pressing Enter
                from selenium.webdriver.common.keys import Keys

                search_input.send_keys(Keys.RETURN)
                logger.debug("Pressed Enter to search")

            # Wait for results to load
            time.sleep(3)

            # Extract information from results
            pinyin = self._extract_pinyin_selenium()
            audio_url = self._extract_audio_url_selenium()
            definition = self._extract_definition_selenium()

            # Check if we found meaningful results
            word_found = self._check_word_exists_selenium(word)

            result["available"] = word_found and (pinyin or audio_url or definition)
            result["pinyin"] = pinyin
            result["audio_url"] = audio_url
            result["definition"] = definition
            result["url"] = self.driver.current_url

            logger.info(f"ChinesePod search for '{word}': available={result['available']}")
            if result["available"]:
                logger.info(f"  Pinyin: {pinyin}")
                logger.info(f"  Definition: {definition}")
                logger.info(f"  Audio URL: {audio_url}")

        except TimeoutException:
            result["error"] = f"Timeout waiting for ChinesePod page to load"
            logger.error(result["error"])
        except WebDriverException as e:
            result["error"] = f"WebDriver error: {e}"
            logger.error(result["error"])
        except Exception as e:
            result["error"] = f"Unexpected error: {e}"
            logger.error(result["error"])

        return result

    def _check_word_exists_selenium(self, word: str) -> bool:
        """Check if the word appears in the current page results."""
        try:
            page_source = self.driver.page_source
            return word in page_source
        except:
            return False

    def _extract_pinyin_selenium(self) -> Optional[str]:
        """Extract pinyin from the current page using Selenium."""
        pinyin_selectors = [
            ".pinyin",
            ".pronunciation",
            ".romanization",
            "[data-pinyin]",
            ".phonetic",
            '*[class*="pinyin"]',
            '*[class*="pronunciation"]',
        ]

        for selector in pinyin_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        text = element.text.strip()
                        if text and len(text) < 50:  # Reasonable pinyin length
                            return text
            except:
                continue

        # Look for pinyin patterns in visible text
        try:
            visible_text = self.driver.find_element(By.TAG_NAME, "body").text
            tone_pattern = r"[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ\s]{2,30}"
            matches = re.findall(tone_pattern, visible_text)

            for match in matches:
                match = match.strip()
                if re.search(r"[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]", match) and len(match.split()) <= 5:
                    return match
        except:
            pass

        return None

    def _extract_audio_url_selenium(self) -> Optional[str]:
        """Extract audio URL from the current page using Selenium."""
        # Look for audio elements
        try:
            audio_elements = self.driver.find_elements(By.TAG_NAME, "audio")
            for audio in audio_elements:
                src = audio.get_attribute("src")
                if src:
                    return src
        except:
            pass

        # Look for source elements
        try:
            source_elements = self.driver.find_elements(By.TAG_NAME, "source")
            for source in source_elements:
                src = source.get_attribute("src")
                if src and any(ext in src.lower() for ext in [".mp3", ".wav", ".ogg"]):
                    return src
        except:
            pass

        # Look for play buttons or elements with audio data
        audio_selectors = [
            "*[data-audio]",
            "*[data-audio-url]",
            "*[data-sound]",
            "*[data-mp3]",
            ".play-button",
            ".audio-button",
            '*[class*="play"]',
            '*[class*="audio"]',
        ]

        for selector in audio_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    for attr in ["data-audio", "data-audio-url", "data-sound", "data-mp3", "data-src"]:
                        audio_url = element.get_attribute(attr)
                        if audio_url:
                            return audio_url
            except:
                continue

        return None

    def _extract_definition_selenium(self) -> Optional[str]:
        """Extract English definition from the current page using Selenium."""
        definition_selectors = [
            ".definition",
            ".meaning",
            ".translation",
            ".english",
            ".def",
            ".gloss",
            '*[class*="definition"]',
            '*[class*="meaning"]',
            '*[class*="translation"]',
        ]

        for selector in definition_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        text = element.text.strip()
                        if text and len(text) > 2 and len(text) < 200:  # Reasonable definition length
                            return text
            except:
                continue

        return None


class ChinesePodChecker:
    """Checker for ChinesePod dictionary pronunciation availability."""

    def __init__(self, timeout: int = 10):
        """Initialize the ChinesePod checker.

        Args:
            timeout: Request timeout in seconds
        """
        self.base_url = "https://www.chinesepod.com/dictionary"
        self.timeout = timeout
        self._session = requests.Session()

        # Set user agent to avoid blocking
        self._session.headers.update(
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
        )

    def check_pronunciation_available(self, word: str, try_alternatives: bool = True) -> Dict[str, Any]:
        """Check if pronunciation is available for a Chinese word on ChinesePod.

        Args:
            word: Chinese word to check

        Returns:
            Dictionary containing:
            - available: bool - whether pronunciation is available
            - url: str - the URL that was checked
            - pinyin: str or None - pinyin if found
            - audio_url: str or None - direct audio URL if found
            - definition: str or None - English definition if found
            - error: str or None - error message if failed
        """
        result = {"available": False, "url": None, "pinyin": None, "audio_url": None, "definition": None, "error": None}

        # Try multiple URL patterns
        urls_to_try = [
            f"{self.base_url}?search={quote(word)}",
            f"https://www.chinesepod.com/dictionary/english-chinese/{quote(word)}",
            f"https://chinesepod.com/dictionary/english-chinese/{quote(word)}",
            f"https://www.chinesepod.com/tools/glossary/{quote(word)}",
        ]

        if not try_alternatives:
            urls_to_try = urls_to_try[:1]  # Only try the first URL

        last_error = None

        for url_attempt in urls_to_try:
            try:
                result["url"] = url_attempt
                logger.debug(f"Checking ChinesePod for word: {word}")
                logger.debug(f"URL: {url_attempt}")

                # Make request
                response = self._session.get(url_attempt, timeout=self.timeout, allow_redirects=True)
                response.raise_for_status()

                logger.debug(f"Final URL after redirects: {response.url}")
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Content length: {len(response.content)}")

                # Parse HTML
                soup = BeautifulSoup(response.content, "html.parser")

                # Debug: Check if we got a proper page
                title = soup.find("title")
                if title:
                    logger.debug(f"Page title: {title.get_text()}")

                # Check for common indicators that the page loaded properly
                if "bootstrap" in response.text.lower() and len(response.text) < 50000:
                    # Likely just CSS/bootstrap - page didn't load properly
                    logger.warning(f"ChinesePod page may not have loaded properly for '{word}' at {url_attempt}")
                    continue  # Try next URL

                # Check if the word was found by looking for key elements
                word_found = self._check_word_exists(soup, word)

                if not word_found:
                    logger.debug(f"Word '{word}' not found at {url_attempt}")
                    continue  # Try next URL

                # Extract pronunciation information
                pinyin = self._extract_pinyin(soup)
                audio_url = self._extract_audio_url(soup, response.url)
                definition = self._extract_definition(soup)

                # Mark as available if we found the word and have audio
                result["available"] = bool(audio_url)
                result["pinyin"] = pinyin
                result["audio_url"] = audio_url
                result["definition"] = definition

                logger.info(f"ChinesePod check for '{word}': available={result['available']} at {url_attempt}")
                return result  # Success! Return immediately

            except requests.exceptions.RequestException as e:
                last_error = f"Network error checking ChinesePod at {url_attempt}: {e}"
                logger.debug(last_error)
                continue  # Try next URL

            except Exception as e:
                last_error = f"Unexpected error checking ChinesePod at {url_attempt}: {e}"
                logger.debug(last_error)
                continue  # Try next URL

        # All URLs failed
        if last_error:
            logger.error(f"All ChinesePod URLs failed for '{word}'. Last error: {last_error}")
            result["error"] = last_error
        else:
            logger.error(f"No ChinesePod URLs worked for '{word}'")

        return result

    def _check_word_exists(self, soup: BeautifulSoup, word: str) -> bool:
        """Check if the word exists in the dictionary page."""
        # ChinesePod appears to redirect to main dictionary page for most searches
        # Look for indicators that this is a meaningful dictionary response

        page_text = soup.get_text().lower()

        # Check for dictionary-specific content
        dictionary_indicators = [
            "pronunciation",
            "pinyin",
            "definition",
            "chinese",
            "dictionary",
            "vocabulary",
            "translation",
        ]

        has_dictionary_content = any(indicator in page_text for indicator in dictionary_indicators)

        # Check if the actual word appears in the page
        word_appears = word in soup.get_text()

        # More lenient check - if we're on a dictionary page and it's not just the homepage
        title = soup.find("title")
        title_text = title.get_text().lower() if title else ""

        is_dictionary_page = "dictionary" in title_text
        is_not_homepage = "start learning" not in title_text

        # Return True if we have dictionary content and either the word appears or it's a proper dictionary page
        return has_dictionary_content and (word_appears or (is_dictionary_page and is_not_homepage))

    def _extract_pinyin(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract pinyin pronunciation from the page."""
        # Common selectors where pinyin might appear
        pinyin_selectors = [".pinyin", ".pronunciation", ".romanization", "[data-pinyin]", ".phonetic"]

        for selector in pinyin_selectors:
            element = soup.select_one(selector)
            if element:
                pinyin_text = element.get_text(strip=True)
                # Clean up pinyin (remove extra whitespace, brackets, etc.)
                pinyin_clean = re.sub(r"[^\w\s\u0101-\u017F]", "", pinyin_text).strip()
                if pinyin_clean:
                    return pinyin_clean

        # Look for pinyin in data attributes
        elements_with_pinyin = soup.find_all(attrs={"data-pinyin": True})
        if elements_with_pinyin:
            return elements_with_pinyin[0]["data-pinyin"]

        # Pattern-based search for pinyin in text
        # Look for tone-marked pinyin (ā á ǎ à etc.)
        tone_pattern = r"[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ\s]+"
        page_text = soup.get_text()
        matches = re.findall(tone_pattern, page_text)

        for match in matches:
            match = match.strip()
            # Simple heuristic: if it contains tone marks and is reasonable length
            if re.search(r"[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]", match) and 2 <= len(match) <= 30:
                return match

        return None

    def _extract_audio_url(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Extract audio URL from the page."""
        # Look for audio elements
        audio_elements = soup.find_all("audio")
        for audio in audio_elements:
            src = audio.get("src")
            if src:
                return urljoin(base_url, src)

        # Look for source elements within audio
        source_elements = soup.find_all("source")
        for source in source_elements:
            src = source.get("src")
            if src and any(ext in src.lower() for ext in [".mp3", ".wav", ".ogg"]):
                return urljoin(base_url, src)

        # Look for data attributes that might contain audio URLs
        audio_data_attrs = ["data-audio", "data-audio-url", "data-sound", "data-pronunciation", "data-mp3"]

        for attr in audio_data_attrs:
            element = soup.find(attrs={attr: True})
            if element:
                audio_url = element[attr]
                if audio_url:
                    return urljoin(base_url, audio_url)

        # Look for links to audio files
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            if any(ext in href.lower() for ext in [".mp3", ".wav", ".ogg"]):
                return urljoin(base_url, href)

        # Look for play buttons or audio controls that might have URLs in onclick, etc.
        play_buttons = soup.find_all(
            ["button", "span", "div"],
            class_=lambda x: x and any(term in x.lower() for term in ["play", "audio", "sound"]),
        )

        for button in play_buttons:
            # Check various attributes that might contain audio URLs
            for attr in ["onclick", "data-url", "data-src", "data-audio"]:
                if button.get(attr):
                    attr_value = button[attr]
                    # Extract URL from JavaScript or direct reference
                    url_match = re.search(r'https?://[^\s\'"]+\.(?:mp3|wav|ogg)', attr_value)
                    if url_match:
                        return url_match.group(0)

        return None

    def _extract_definition(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract English definition from the page."""
        # Common selectors for definitions
        definition_selectors = [".definition", ".meaning", ".translation", ".english", ".def", ".gloss"]

        for selector in definition_selectors:
            element = soup.select_one(selector)
            if element:
                def_text = element.get_text(strip=True)
                # Clean up definition (remove extra whitespace)
                def_clean = " ".join(def_text.split())
                if def_clean and len(def_clean) > 2:  # Reasonable definition length
                    return def_clean

        # Look in meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return meta_desc["content"].strip()

        return None

    def is_available(self) -> bool:
        """Check if ChinesePod service is available."""
        try:
            response = self._session.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False


def check_chinesepod_pronunciation(word: str, timeout: int = 10, use_selenium: bool = None) -> Dict[str, Any]:
    """Convenience function to check ChinesePod pronunciation availability.

    Args:
        word: Chinese word to check
        timeout: Request timeout in seconds
        use_selenium: Force use of Selenium (None = auto-detect, True = force Selenium, False = force requests)

    Returns:
        Dictionary with check results
    """
    # Auto-detect whether to use Selenium
    if use_selenium is None:
        use_selenium = SELENIUM_AVAILABLE

    if use_selenium and SELENIUM_AVAILABLE:
        # Use Selenium for JavaScript-heavy sites
        try:
            with ChinesePodSeleniumChecker(timeout=timeout) as checker:
                return checker.check_pronunciation_available(word)
        except ChinesePodError as e:
            logger.warning(f"Selenium checker failed: {e}, falling back to requests")
            use_selenium = False

    if not use_selenium:
        # Fall back to requests-based checker
        checker = ChinesePodChecker(timeout=timeout)
        return checker.check_pronunciation_available(word)

    return {
        "available": False,
        "url": None,
        "pinyin": None,
        "audio_url": None,
        "definition": None,
        "error": "Neither Selenium nor requests method available",
    }


def check_chinesepod_service_available(timeout: int = 5) -> bool:
    """Simple check if ChinesePod service is online and accessible.

    Args:
        timeout: Request timeout in seconds

    Returns:
        bool: True if service is accessible, False otherwise
    """
    try:
        checker = ChinesePodChecker(timeout=timeout)
        return checker.is_available()
    except:
        return False


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        word = sys.argv[1]
        result = check_chinesepod_pronunciation(word)

        print(f"Word: {word}")
        print(f"Available: {result['available']}")
        print(f"URL: {result['url']}")
        print(f"Pinyin: {result['pinyin']}")
        print(f"Audio URL: {result['audio_url']}")
        print(f"Definition: {result['definition']}")
        if result["error"]:
            print(f"Error: {result['error']}")
    else:
        # Test with example
        test_words = ["警察", "你好", "学习"]
        for word in test_words:
            print(f"\n--- Testing: {word} ---")
            result = check_chinesepod_pronunciation(word)
            print(f"Available: {result['available']}")
            if result["pinyin"]:
                print(f"Pinyin: {result['pinyin']}")
