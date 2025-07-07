"""Audio generation module with multiple TTS providers."""

import os
import hashlib
import subprocess
import tempfile
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
    
    def _get_cache_filename(self, text: str, provider: str) -> Path:
        """Generate a cache filename based on text and provider."""
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        return self.cache_dir / f"{provider}_{text_hash}.mp3"
    
    def _is_cached(self, text: str, provider: str) -> bool:
        """Check if audio is already cached."""
        return self._get_cache_filename(text, provider).exists()
    
    def _get_cached_path(self, text: str, provider: str) -> Optional[str]:
        """Get path to cached audio file."""
        cache_file = self._get_cache_filename(text, provider)
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
    
    def generate_with_cache(self, text: str, output_file: Optional[str] = None) -> Optional[str]:
        """Generate audio with caching support."""
        provider = self.get_provider_name()
        
        # Check cache first
        if self._is_cached(text, provider):
            cached_path = self._get_cached_path(text, provider)
            logger.info(f"Using cached audio for '{text}' from {provider}")
            
            # If output_file is specified, copy from cache
            if output_file and cached_path:
                import shutil
                shutil.copy2(cached_path, output_file)
                return output_file
            return cached_path
        
        # Generate new audio
        if not output_file:
            output_file = str(self._get_cache_filename(text, provider))
        
        result = self.generate_audio(text, output_file)
        
        # Cache the result if successful and not already in cache location
        if result and result != str(self._get_cache_filename(text, provider)):
            cache_file = self._get_cache_filename(text, provider)
            import shutil
            shutil.copy2(result, cache_file)
        
        return result


class AzureSpeechGenerator(AudioGenerator):
    """Azure Speech Services TTS generator."""
    
    def __init__(self, subscription_key: str, region: str, cache_dir: Optional[str] = None):
        super().__init__(cache_dir)
        self.subscription_key = subscription_key
        self.region = region
        self.voice_name = "zh-CN-XiaoxiaoNeural"
    
    def is_available(self) -> bool:
        """Check if Azure Speech is available."""
        try:
            import azure.cognitiveservices.speech as speechsdk
            return bool(self.subscription_key and self.region)
        except ImportError:
            return False
    
    def get_provider_name(self) -> str:
        return "azure"
    
    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """Generate audio using Azure Speech Services."""
        if not self.is_available():
            raise TTSProviderNotAvailable("Azure Speech Services not available")
        
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_config = speechsdk.SpeechConfig(
                subscription=self.subscription_key,
                region=self.region
            )
            speech_config.speech_synthesis_voice_name = self.voice_name
            
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=speechsdk.audio.AudioOutputConfig(filename=output_file)
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"Azure TTS generated audio for '{text}'")
                return output_file
            else:
                logger.error(f"Azure TTS failed: {result.reason}")
                return None
                
        except Exception as e:
            logger.error(f"Azure TTS error: {e}")
            return None


class OpenAITTSGenerator(AudioGenerator):
    """OpenAI TTS generator."""
    
    def __init__(self, api_key: str, cache_dir: Optional[str] = None):
        super().__init__(cache_dir)
        self.api_key = api_key
        self.voice = "nova"
        self.model = "tts-1"
    
    def is_available(self) -> bool:
        """Check if OpenAI TTS is available."""
        try:
            import openai
            return bool(self.api_key)
        except ImportError:
            return False
    
    def get_provider_name(self) -> str:
        return "openai"
    
    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """Generate audio using OpenAI TTS."""
        if not self.is_available():
            raise TTSProviderNotAvailable("OpenAI TTS not available")
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            response = client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            
            response.stream_to_file(output_file)
            logger.info(f"OpenAI TTS generated audio for '{text}'")
            return output_file
            
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            return None


class AmazonPollyGenerator(AudioGenerator):
    """Amazon Polly TTS generator."""
    
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, 
                 region: str = "us-east-1", cache_dir: Optional[str] = None):
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
    
    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """Generate audio using Amazon Polly."""
        if not self.is_available():
            raise TTSProviderNotAvailable("Amazon Polly not available")
        
        try:
            import boto3
            
            polly = boto3.client(
                'polly',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            )
            
            response = polly.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=self.voice_id,
                LanguageCode=self.language_code
            )
            
            with open(output_file, 'wb') as file:
                file.write(response['AudioStream'].read())
            
            logger.info(f"Amazon Polly generated audio for '{text}'")
            return output_file
            
        except Exception as e:
            logger.error(f"Amazon Polly error: {e}")
            return None


class ESpeakGenerator(AudioGenerator):
    """eSpeak-NG offline TTS generator."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        super().__init__(cache_dir)
        self.speed = 150
        self.voice = "zh"
    
    def is_available(self) -> bool:
        """Check if eSpeak-NG is available."""
        try:
            result = subprocess.run(['espeak-ng', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_provider_name(self) -> str:
        return "espeak"
    
    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """Generate audio using eSpeak-NG."""
        if not self.is_available():
            raise TTSProviderNotAvailable("eSpeak-NG not available")
        
        try:
            # Ensure output file has .wav extension for espeak
            if not output_file.endswith('.wav'):
                wav_file = output_file.replace('.mp3', '.wav')
            else:
                wav_file = output_file
            
            result = subprocess.run([
                'espeak-ng',
                '-v', self.voice,
                '-s', str(self.speed),
                '-w', wav_file,
                text
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Convert WAV to MP3 if needed
                if output_file.endswith('.mp3') and wav_file != output_file:
                    self._convert_wav_to_mp3(wav_file, output_file)
                    os.remove(wav_file)  # Clean up WAV file
                    return output_file
                else:
                    logger.info(f"eSpeak-NG generated audio for '{text}'")
                    return wav_file
            else:
                logger.error(f"eSpeak-NG failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"eSpeak-NG error: {e}")
            return None
    
    def _convert_wav_to_mp3(self, wav_file: str, mp3_file: str):
        """Convert WAV to MP3 using ffmpeg if available."""
        try:
            subprocess.run([
                'ffmpeg', '-i', wav_file, '-acodec', 'mp3', mp3_file, '-y'
            ], capture_output=True, timeout=30)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # If ffmpeg not available, just rename the file
            import shutil
            shutil.move(wav_file, mp3_file)


class ForvoGenerator(AudioGenerator):
    """Forvo community pronunciation generator."""
    
    def __init__(self, api_key: str, cache_dir: Optional[str] = None, use_paid_api: bool = True):
        super().__init__(cache_dir)
        self.api_key = api_key
        self.language = "zh"
        # Note: Forvo uses the same endpoint for both free and paid APIs
        # The difference is in rate limits and features, not the URL
        self.base_url = "https://apifree.forvo.com"
        self.use_paid_api = use_paid_api
    
    def is_available(self) -> bool:
        """Check if Forvo API is available."""
        return bool(self.api_key)
    
    def get_provider_name(self) -> str:
        return "forvo"
    
    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """Download audio from Forvo."""
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
            logger.info(f"Forvo API response data: {data}")
            
            # Check for API error messages
            if 'error' in data:
                logger.error(f"Forvo API error: {data['error']}")
                return None
            
            if data.get('items'):
                # Get the highest-rated pronunciation
                best_pronunciation = max(data['items'], key=lambda x: x.get('num_votes', 0))
                audio_url = best_pronunciation.get('pathmp3')
                
                if audio_url:
                    logger.info(f"Downloading audio from: {audio_url}")
                    # Download the audio file
                    audio_response = requests.get(audio_url, timeout=30)
                    audio_response.raise_for_status()
                    
                    with open(output_file, 'wb') as f:
                        f.write(audio_response.content)
                    
                    logger.info(f"Forvo downloaded audio for '{text}' to {output_file}")
                    return output_file
                else:
                    logger.warning(f"No audio URL found in Forvo response for '{text}'")
                    return None
            else:
                logger.warning(f"No Forvo pronunciation items found for '{text}'")
                return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Forvo network error: {e}")
            return None
        except Exception as e:
            logger.error(f"Forvo unexpected error: {e}")
            return None


class WiktionaryGenerator(AudioGenerator):
    """Wiktionary public domain audio generator."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        super().__init__(cache_dir)
    
    def is_available(self) -> bool:
        """Wiktionary is always available."""
        return True
    
    def get_provider_name(self) -> str:
        return "wiktionary"
    
    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """Download audio from Wiktionary."""
        try:
            from bs4 import BeautifulSoup
            
            # Search Wiktionary for the word
            url = f"https://en.wiktionary.org/wiki/{text}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for Chinese audio files
            audio_elements = soup.find_all('source', {'type': 'audio/ogg'})
            
            for audio in audio_elements:
                src = audio.get('src', '')
                if 'zh-' in src or 'cmn-' in src:  # Chinese audio
                    # Convert relative URL to absolute
                    if src.startswith('//'):
                        audio_url = 'https:' + src
                    elif src.startswith('/'):
                        audio_url = 'https://en.wiktionary.org' + src
                    else:
                        audio_url = src
                    
                    # Download the audio
                    audio_response = requests.get(audio_url, timeout=30)
                    audio_response.raise_for_status()
                    
                    with open(output_file, 'wb') as f:
                        f.write(audio_response.content)
                    
                    logger.info(f"Wiktionary downloaded audio for '{text}'")
                    return output_file
            
            logger.warning(f"No Wiktionary audio found for '{text}'")
            return None
            
        except Exception as e:
            logger.error(f"Wiktionary error: {e}")
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
                cache_dir=cache_dir
            )
        elif provider == "openai":
            return OpenAITTSGenerator(
                api_key=config.get("api_key"),
                cache_dir=cache_dir
            )
        elif provider == "polly":
            return AmazonPollyGenerator(
                aws_access_key_id=config.get("aws_access_key_id"),
                aws_secret_access_key=config.get("aws_secret_access_key"),
                region=config.get("region", "us-east-1"),
                cache_dir=cache_dir
            )
        elif provider == "espeak":
            return ESpeakGenerator(cache_dir=cache_dir)
        elif provider == "forvo":
            return ForvoGenerator(
                api_key=config.get("api_key"),
                cache_dir=cache_dir,
                use_paid_api=config.get("use_paid_api", True)
            )
        elif provider == "wiktionary":
            return WiktionaryGenerator(cache_dir=cache_dir)
        else:
            raise ValueError(f"Unknown audio provider: {provider}")
    
    @staticmethod
    def get_available_providers(config: Dict[str, Dict[str, Any]]) -> list[str]:
        """Get list of available providers based on configuration."""
        available = []
        
        for provider in ["azure", "openai", "polly", "espeak", "forvo", "wiktionary"]:
            try:
                generator = AudioGeneratorFactory.create_generator(
                    provider, config.get(provider, {}), cache_dir=None
                )
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
                    result = generator.generate_with_cache(text, output_file)
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