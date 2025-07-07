"""Audio generation module with multiple TTS providers."""

import os
import hashlib
import subprocess
import tempfile
import platform
import shutil
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any
import logging

import requests

logger = logging.getLogger(__name__)


class AudioGeneratorError(Exception):
    """Base exception for audio generation errors."""

    pass


class TTSProviderNotAvailable(AudioGeneratorError):
    """Raised when a TTS provider is not available or configured."""

    pass


class AudioGenerator(ABC):
    """Abstract base class for audio generators."""

    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path("audio_cache")
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_filename(self, text: str, provider: str, details: Optional[str] = None) -> Path:
        """Generate a cache filename based on text, provider, and optional details."""
        # Sanitize the Chinese text for filename (remove unsafe characters)
        safe_text = re.sub(r'[<>:"/\\|?*]', "", text)
        safe_text = safe_text.replace(" ", "_")

        # Build filename components
        filename_parts = [safe_text, provider]

        # Add details if provided (e.g., Forvo username)
        if details:
            safe_details = re.sub(r'[<>:"/\\|?*]', "", details)
            safe_details = safe_details.replace(" ", "_")
            filename_parts.append(safe_details)

        # Add hash to avoid conflicts and ensure uniqueness
        content_hash = hashlib.md5(f"{text}_{provider}_{details or ''}".encode("utf-8")).hexdigest()[:8]
        filename_parts.append(content_hash)

        filename = "_".join(filename_parts) + ".mp3"
        return self.cache_dir / filename

    def _is_cached(self, text: str, provider: str, details: Optional[str] = None) -> bool:
        """Check if audio is already cached."""
        return self._get_cache_filename(text, provider, details).exists()

    def _get_cached_path(self, text: str, provider: str, details: Optional[str] = None) -> Optional[str]:
        """Get path to cached audio file."""
        cache_file = self._get_cache_filename(text, provider, details)
        return str(cache_file) if cache_file.exists() else None

    @abstractmethod
    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """Generate audio for the given text."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this audio generator is available."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of this provider."""
        pass

    def generate_with_cache(
        self, text: str, output_file: Optional[str] = None, cache_details: Optional[str] = None
    ) -> Optional[str]:
        """Generate audio with caching support."""
        provider = self.get_provider_name()

        # Check cache first
        if self._is_cached(text, provider, cache_details):
            cached_path = self._get_cached_path(text, provider, cache_details)
            logger.info(f"Using cached audio for '{text}' from {provider}")

            # If output_file is specified, copy from cache
            if output_file and cached_path:
                import shutil

                shutil.copy2(cached_path, output_file)
                return output_file
            return cached_path

        # Generate new audio
        if not output_file:
            output_file = str(self._get_cache_filename(text, provider, cache_details))

        result = self.generate_audio(text, output_file)

        # Cache the result if successful and not already in cache location
        if result and result != str(self._get_cache_filename(text, provider, cache_details)):
            cache_file = self._get_cache_filename(text, provider, cache_details)
            import shutil

            shutil.copy2(result, cache_file)

        return result


class AzureSpeechGenerator(AudioGenerator):
    """Azure Speech Services TTS generator."""

    def __init__(
        self,
        subscription_key: str,
        region: str,
        cache_dir: Optional[str] = None,
        voice_name: Optional[str] = None,
        speaking_rate: float = 0.85,
    ):
        super().__init__(cache_dir)
        self.subscription_key = subscription_key
        self.region = region
        # Available voices for better quality:
        # zh-CN-XiaochenNeural - conversational optimized (recommended)
        # zh-CN-XiaoyanNeural - customer service optimized
        # zh-CN-XiaoxiaoMultilingualNeural - multilingual with styles
        # zh-CN-YunjieNeural - latest conversational (preview)
        self.voice_name = voice_name or "zh-CN-XiaochenNeural"
        self.speaking_rate = speaking_rate  # 0.5-2.0, default 0.85 (15% slower for clarity)

    def is_available(self) -> bool:
        """Check if Azure Speech is available."""
        try:
            import azure.cognitiveservices.speech as speechsdk

            return bool(self.subscription_key and self.region)
        except ImportError:
            return False

    def get_provider_name(self) -> str:
        return "azure"

    def get_cache_details(self) -> str:
        """Get cache details for Azure (voice name)."""
        return self.voice_name

    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """Generate audio using Azure Speech Services with SSML for enhanced quality."""
        if not self.is_available():
            raise TTSProviderNotAvailable("Azure Speech Services not available")

        try:
            import azure.cognitiveservices.speech as speechsdk

            speech_config = speechsdk.SpeechConfig(subscription=self.subscription_key, region=self.region)
            # Set higher quality audio format (48kHz vs default 16kHz)
            speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
            )

            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config, audio_config=speechsdk.audio.AudioOutputConfig(filename=output_file)
            )

            # Create enhanced SSML for better pronunciation and pacing
            ssml = self._create_enhanced_ssml(text)
            logger.debug(f"Using enhanced SSML for '{text}' with voice {self.voice_name}")

            result = synthesizer.speak_ssml_async(ssml).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"Azure TTS generated enhanced audio for '{text}' using {self.voice_name}")
                return output_file
            else:
                logger.error(f"Azure TTS failed: {result.reason}")
                if result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    logger.error(f"Cancellation reason: {cancellation_details.reason}")
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        logger.error(f"Error details: {cancellation_details.error_details}")
                return None

        except Exception as e:
            logger.error(f"Azure TTS error: {e}")
            return None

    def _create_enhanced_ssml(self, text: str) -> str:
        """Create enhanced SSML for better pronunciation and naturalness."""
        # Calculate rate percentage (0.85 = 85% of normal speed = -15%)
        rate_percentage = (self.speaking_rate - 1.0) * 100
        rate_str = f"{rate_percentage:+.0f}%" if rate_percentage != 0 else "default"

        # Enhanced SSML with prosody control, pauses, and style
        ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
                   xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">
    <voice name="{self.voice_name}">
        <mstts:express-as style="calm" styledegree="0.8">
            <prosody rate="{rate_str}" pitch="+3%" volume="+10%">
                {self._add_pronunciation_hints(text)}
            </prosody>
        </mstts:express-as>
    </voice>
</speak>"""

        return ssml

    def _add_pronunciation_hints(self, text: str) -> str:
        """Add pronunciation hints and pauses for better clarity."""
        import re

        # Add slight pauses after Chinese punctuation for better pacing
        text = re.sub(r"([。！？])", r'\1<break time="400ms"/>', text)  # Full stop, exclamation, question
        text = re.sub(r"([，、；：])", r'\1<break time="200ms"/>', text)  # Comma, enumeration comma, semicolon, colon

        # For single characters, add moderate emphasis for clarity
        if len(text) <= 2:
            text = f'<emphasis level="moderate">{text}</emphasis>'

        # For compound words (3-4 characters), add slight pause between logical components
        elif len(text) == 4:
            # Common pattern: split 4-character words in the middle
            text = text[:2] + '<break time="100ms"/>' + text[2:]

        return text


class AmazonPollyGenerator(AudioGenerator):
    """Amazon Polly TTS generator."""

    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region: str = "us-east-1",
        cache_dir: Optional[str] = None,
    ):
        super().__init__(cache_dir)
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region
        self.voice_id = "Zhiyu"
        self.language_code = "cmn-CN"

    def is_available(self) -> bool:
        """Check if Amazon Polly is available."""
        try:
            import boto3

            return bool(self.aws_access_key_id and self.aws_secret_access_key)
        except ImportError:
            return False

    def get_provider_name(self) -> str:
        return "polly"

    def get_cache_details(self) -> str:
        """Get cache details for Polly (voice ID)."""
        return self.voice_id

    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """Generate audio using Amazon Polly."""
        if not self.is_available():
            raise TTSProviderNotAvailable("Amazon Polly not available")

        try:
            import boto3

            polly = boto3.client(
                "polly",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region,
            )

            response = polly.synthesize_speech(
                Text=text, OutputFormat="mp3", VoiceId=self.voice_id, LanguageCode=self.language_code
            )

            with open(output_file, "wb") as file:
                file.write(response["AudioStream"].read())

            logger.info(f"Amazon Polly generated audio for '{text}'")
            return output_file

        except Exception as e:
            logger.error(f"Amazon Polly error: {e}")
            return None


class ForvoGenerator(AudioGenerator):
    """Forvo community pronunciation generator with smart user selection."""

    def __init__(
        self,
        api_key: str,
        cache_dir: Optional[str] = None,
        use_paid_api: bool = True,
        preferred_users: Optional[list[str]] = None,
        download_all_when_no_preferred: bool = True,
        interactive_selection: bool = True,
    ):
        super().__init__(cache_dir)
        self.api_key = api_key
        self.language = "zh"
        # Note: Forvo uses the same endpoint for both free and paid APIs
        # The difference is in rate limits and features, not the URL
        self.base_url = "https://apifree.forvo.com"
        self.use_paid_api = use_paid_api
        self.preferred_users = preferred_users or []
        self.download_all_when_no_preferred = download_all_when_no_preferred
        self.interactive_selection = interactive_selection

    def is_available(self) -> bool:
        """Check if Forvo API is available."""
        return bool(self.api_key)

    def get_provider_name(self) -> str:
        return "forvo"

    def _find_cached_forvo_audio(self, text: str) -> Optional[str]:
        """Find any cached Forvo audio for this text, regardless of username."""
        # Look for any existing Forvo cache files for this text
        safe_text = re.sub(r'[<>:"/\\|?*]', "", text).replace(" ", "_")
        pattern = f"{safe_text}_forvo_*.mp3"
        cache_files = list(self.cache_dir.glob(pattern))
        return str(cache_files[0]) if cache_files else None

    def _format_pronunciation_info(self, pronunciation: Dict) -> str:
        """Format pronunciation information for display."""
        username = pronunciation.get("username", "unknown")
        sex = pronunciation.get("sex", "?")
        country = pronunciation.get("country", "unknown")
        votes = pronunciation.get("num_votes", 0)
        positive_votes = pronunciation.get("num_positive_votes", 0)
        rating = pronunciation.get("rate", 0)

        # Colored gender icons
        if sex == "f":
            gender_icon = "\033[95m♀\033[0m"  # Magenta/pink for female
        elif sex == "m":
            gender_icon = "\033[94m♂\033[0m"  # Blue for male
        else:
            gender_icon = "\033[90m?\033[0m"  # Gray for unknown

        # Country flags mapping
        country_flags = {
            "China": "🇨🇳",
            "Taiwan": "🇹🇼",
            "Hong Kong": "🇭🇰",
            "Singapore": "🇸🇬",
            "United States": "🇺🇸",
            "Canada": "🇨🇦",
            "United Kingdom": "🇬🇧",
            "Australia": "🇦🇺",
            "New Zealand": "🇳🇿",
            "Japan": "🇯🇵",
            "South Korea": "🇰🇷",
            "Thailand": "🇹🇭",
            "Malaysia": "🇲🇾",
            "Philippines": "🇵🇭",
            "Indonesia": "🇮🇩",
            "Vietnam": "🇻🇳",
            "Germany": "🇩🇪",
            "France": "🇫🇷",
            "Spain": "🇪🇸",
            "Italy": "🇮🇹",
            "Netherlands": "🇳🇱",
            "Brazil": "🇧🇷",
            "Mexico": "🇲🇽",
            "Argentina": "🇦🇷",
            "Russia": "🇷🇺",
            "India": "🇮🇳",
        }

        # Get country flag or fallback to country name
        country_display = country_flags.get(country, f"🏳️ {country}")

        # Rating stars
        stars = "⭐" * min(5, max(0, int(rating))) if rating > 0 else ""

        # Preferred user indicator
        preferred = " [PREFERRED]" if username in self.preferred_users else ""

        return f"{username} ({gender_icon} {country_display}) - {votes} votes, rating: {rating:.1f} {stars}{preferred}"

    def _select_best_pronunciation(self, pronunciations: list[Dict], text: str) -> Optional[Dict]:
        """Select the best pronunciation based on preferences."""
        if not pronunciations:
            return None

        # Check for preferred users in order
        for preferred_user in self.preferred_users:
            for pronunciation in pronunciations:
                if pronunciation.get("username") == preferred_user:
                    logger.info(f"Found preferred user '{preferred_user}' for '{text}'")
                    return pronunciation

        # No preferred users found
        if not self.download_all_when_no_preferred:
            # Fall back to highest-rated pronunciation
            best = max(pronunciations, key=lambda x: (x.get("num_positive_votes", 0), x.get("num_votes", 0)))
            logger.info(f"No preferred users found for '{text}', using highest-rated: {best.get('username')}")
            return best

        # Interactive selection if enabled
        if self.interactive_selection and len(pronunciations) > 1:
            return self._interactive_pronunciation_selection(pronunciations, text)
        else:
            # Just use the first one if interactive selection is disabled
            return pronunciations[0]

    def _play_audio(self, file_path: str) -> bool:
        """Play audio file with cross-platform support."""
        try:
            # Try playsound3 first
            try:
                from playsound3 import playsound

                playsound(file_path)
                return True
            except ImportError:
                logger.debug("playsound3 not available, falling back to system commands")

            # Fallback to system commands
            system = platform.system()

            if system == "Darwin":  # macOS
                subprocess.run(["afplay", file_path], check=True, capture_output=True)
                return True
            elif system == "Linux":
                # Try mpg123 first, then mpv
                for player, args in [("mpg123", ["-q"]), ("mpv", ["--no-video"]), ("ffplay", ["-nodisp", "-autoexit"])]:
                    try:
                        subprocess.run([player] + args + [file_path], check=True, capture_output=True)
                        return True
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
            elif system == "Windows":
                # Try ffplay if available
                try:
                    subprocess.run(["ffplay", "-nodisp", "-autoexit", file_path], check=True, capture_output=True)
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass

            return False

        except Exception as e:
            logger.warning(f"Failed to play audio: {e}")
            return False

    def _download_pronunciation_preview(self, pronunciation: Dict, text: str) -> Optional[str]:
        """Download pronunciation to temporary file for preview."""
        audio_url = pronunciation.get("pathmp3")
        if not audio_url:
            return None

        try:
            # Create temporary file
            username = pronunciation.get("username", "unknown")
            temp_file = tempfile.NamedTemporaryFile(suffix=f"_{username}_{text[:10]}.mp3", delete=False)
            temp_file.close()

            # Download audio
            logger.debug(f"Downloading preview audio from: {audio_url}")
            audio_response = requests.get(audio_url, timeout=30)
            audio_response.raise_for_status()

            with open(temp_file.name, "wb") as f:
                f.write(audio_response.content)

            return temp_file.name

        except Exception as e:
            logger.warning(f"Failed to download preview audio: {e}")
            return None

    def _cleanup_preview_files(self, preview_files: list[str]):
        """Clean up temporary preview files."""
        for file_path in preview_files:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logger.warning(f"Failed to cleanup preview file {file_path}: {e}")

    def _interactive_pronunciation_selection(self, pronunciations: list[Dict], text: str) -> Optional[Dict]:
        """Allow interactive selection of pronunciation with audio preview."""
        print(f"\n🎵 {text} - Found {len(pronunciations)} pronunciations:")

        for i, pronunciation in enumerate(pronunciations, 1):
            info = self._format_pronunciation_info(pronunciation)
            print(f"{i:2d}. {info}")

        print(f"\nCommands: p<number> to preview, <number> to select, 's' to skip")
        print(f"Example: 'p1' to preview option 1, '1' to select option 1")

        preview_files = []  # Track temporary files for cleanup

        try:
            while True:
                try:
                    choice = input(f"\nChoice: ").strip().lower()

                    if choice == "s":
                        logger.info(f"User skipped pronunciation selection for '{text}'")
                        return None

                    # Handle preview commands (p1, p2, etc.)
                    if choice.startswith("p") and len(choice) > 1:
                        try:
                            preview_num = int(choice[1:])
                            if 1 <= preview_num <= len(pronunciations):
                                pronunciation = pronunciations[preview_num - 1]
                                username = pronunciation.get("username", "unknown")

                                print(f"🔊 Downloading and playing pronunciation by {username}...")

                                # Download to temporary file
                                temp_file = self._download_pronunciation_preview(pronunciation, text)
                                if temp_file:
                                    preview_files.append(temp_file)

                                    # Try to play the audio
                                    if self._play_audio(temp_file):
                                        print(f"✅ Played pronunciation by {username}")

                                        # Ask for confirmation
                                        confirm = input(f"Select this pronunciation? (y/n): ").strip().lower()
                                        if confirm in ["y", "yes"]:
                                            logger.info(
                                                f"User selected pronunciation by '{username}' for '{text}' after preview"
                                            )
                                            return pronunciation
                                    else:
                                        print(f"❌ Could not play audio (file downloaded but playback failed)")
                                        print(f"You may need to install an audio player or playsound3")
                                else:
                                    print(f"❌ Could not download audio for preview")
                            else:
                                print(f"Please enter a number between 1 and {len(pronunciations)}")
                        except ValueError:
                            print(f"Invalid preview command. Use format: p1, p2, etc.")
                        continue

                    # Handle direct selection (1, 2, etc.)
                    try:
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(pronunciations):
                            selected = pronunciations[choice_num - 1]
                            username = selected.get("username", "unknown")

                            # Ask for confirmation without preview
                            confirm = (
                                input(f"Select pronunciation by {username} without preview? (y/n): ").strip().lower()
                            )
                            if confirm in ["y", "yes"]:
                                logger.info(f"User selected pronunciation by '{username}' for '{text}' without preview")
                                return selected
                        else:
                            print(f"Please enter a number between 1 and {len(pronunciations)}")
                    except ValueError:
                        print("Invalid input. Use: number to select, p<number> to preview, 's' to skip")

                except KeyboardInterrupt:
                    print("\nSkipping pronunciation selection...")
                    return None
        finally:
            # Clean up temporary preview files
            if preview_files:
                self._cleanup_preview_files(preview_files)

    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """Download audio from Forvo with smart user selection."""
        if not self.is_available():
            raise TTSProviderNotAvailable("Forvo API not available")

        try:
            # Get pronunciation URL
            url = f"{self.base_url}/key/{self.api_key}/format/json/action/word-pronunciations/word/{text}/language/{self.language}"
            logger.info(f"Forvo API request: {url}")

            response = requests.get(url, timeout=10)
            logger.info(f"Forvo API response status: {response.status_code}")

            if response.status_code == 401:
                logger.error("Forvo API authentication failed - check your API key")
                return None
            elif response.status_code == 403:
                logger.error("Forvo API access forbidden - check your subscription status")
                return None
            elif response.status_code == 429:
                logger.error("Forvo API rate limit exceeded")
                return None

            response.raise_for_status()

            data = response.json()

            # Check for API error messages
            if "error" in data:
                logger.error(f"Forvo API error: {data['error']}")
                return None

            pronunciations = data.get("items", [])
            if not pronunciations:
                logger.warning(f"No Forvo pronunciation items found for '{text}'")
                return None

            # Select the best pronunciation
            selected_pronunciation = self._select_best_pronunciation(pronunciations, text)
            if not selected_pronunciation:
                logger.info(f"No pronunciation selected for '{text}'")
                return None

            # Get user info for logging and filename
            username = selected_pronunciation.get("username", "unknown")
            audio_url = selected_pronunciation.get("pathmp3")

            if not audio_url:
                logger.warning(f"No audio URL found in selected pronunciation for '{text}'")
                return None

            logger.info(f"Downloading audio from: {audio_url}")
            logger.info(f"Selected pronunciation by: {username}")

            # Download the audio file
            audio_response = requests.get(audio_url, timeout=30)
            audio_response.raise_for_status()

            # Write to output file
            with open(output_file, "wb") as f:
                f.write(audio_response.content)

            logger.info(f"Forvo downloaded audio for '{text}' by '{username}' to {output_file}")
            return output_file

        except requests.exceptions.RequestException as e:
            logger.error(f"Forvo network error: {e}")
            return None
        except Exception as e:
            logger.error(f"Forvo unexpected error: {e}")
            return None

    def generate_with_cache(self, text: str, output_file: Optional[str] = None) -> Optional[str]:
        """Generate audio with Forvo-specific caching that includes username."""
        # Check for any existing cached audio first
        cached_audio = self._find_cached_forvo_audio(text)
        if cached_audio:
            logger.info(f"Using cached Forvo audio for '{text}': {cached_audio}")
            if output_file and output_file != cached_audio:
                import shutil

                shutil.copy2(cached_audio, output_file)
                return output_file
            return cached_audio

        # No cache found, need to download and determine username first
        try:
            # Get pronunciation URL to determine username
            url = f"{self.base_url}/key/{self.api_key}/format/json/action/word-pronunciations/word/{text}/language/{self.language}"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                return None

            data = response.json()
            pronunciations = data.get("items", [])
            if not pronunciations:
                return None

            # Select the best pronunciation to get username
            selected_pronunciation = self._select_best_pronunciation(pronunciations, text)
            if not selected_pronunciation:
                return None

            username = selected_pronunciation.get("username", "unknown")

            # Use new caching system with username as cache_details
            return super().generate_with_cache(text, output_file, username)

        except Exception as e:
            logger.error(f"Forvo cache lookup error: {e}")
            return None


class AudioGeneratorFactory:
    """Factory for creating audio generators."""

    @staticmethod
    def create_generator(provider: str, config: Dict[str, Any], cache_dir: Optional[str] = None) -> AudioGenerator:
        """Create an audio generator based on provider and configuration."""
        if provider == "azure":
            return AzureSpeechGenerator(
                subscription_key=config.get("subscription_key"),
                region=config.get("region"),
                cache_dir=cache_dir,
                voice_name=config.get("voice_name"),
                speaking_rate=config.get("speaking_rate", 0.85),
            )
        elif provider == "polly":
            return AmazonPollyGenerator(
                aws_access_key_id=config.get("aws_access_key_id"),
                aws_secret_access_key=config.get("aws_secret_access_key"),
                region=config.get("region", "us-east-1"),
                cache_dir=cache_dir,
            )
        elif provider == "forvo":
            return ForvoGenerator(
                api_key=config.get("api_key"),
                cache_dir=cache_dir,
                use_paid_api=config.get("use_paid_api", True),
                preferred_users=config.get("preferred_users", []),
                download_all_when_no_preferred=config.get("download_all_when_no_preferred", True),
                interactive_selection=config.get("interactive_selection", True),
            )
        else:
            raise ValueError(f"Unknown audio provider: {provider}")

    @staticmethod
    def get_available_providers(config: Dict[str, Dict[str, Any]]) -> list[str]:
        """Get list of available providers based on configuration."""
        available = []

        for provider in ["azure", "polly", "forvo"]:
            try:
                generator = AudioGeneratorFactory.create_generator(provider, config.get(provider, {}), cache_dir=None)
                if generator.is_available():
                    available.append(provider)
            except Exception:
                pass

        return available


class MultiProviderAudioGenerator:
    """Audio generator that tries multiple providers in order of preference."""

    def __init__(self, providers: list[str], config: Dict[str, Dict[str, Any]], cache_dir: Optional[str] = None):
        self.providers = providers
        self.config = config
        self.cache_dir = cache_dir
        self.generators = {}

        # Initialize generators
        for provider in providers:
            try:
                generator = AudioGeneratorFactory.create_generator(provider, config.get(provider, {}), cache_dir)
                if generator.is_available():
                    self.generators[provider] = generator
                    logger.info(f"Audio provider '{provider}' is available")
                else:
                    logger.warning(f"Audio provider '{provider}' is not available")
            except Exception as e:
                logger.error(f"Failed to initialize audio provider '{provider}': {e}")

    def generate_audio(self, text: str, output_file: Optional[str] = None) -> Optional[str]:
        """Generate audio using the first available provider."""
        for provider in self.providers:
            generator = self.generators.get(provider)
            if generator:
                try:
                    # Get cache details if the generator supports it
                    cache_details = None
                    if hasattr(generator, "get_cache_details"):
                        cache_details = generator.get_cache_details()

                    result = generator.generate_with_cache(text, output_file, cache_details)
                    if result:
                        logger.info(f"Successfully generated audio for '{text}' using {provider}")
                        return result
                except Exception as e:
                    logger.error(f"Provider '{provider}' failed for '{text}': {e}")
                    continue

        logger.error(f"All audio providers failed for '{text}'")
        return None

    def get_available_providers(self) -> list[str]:
        """Get list of available providers."""
        return list(self.generators.keys())
