"""Tests for audio generation functionality."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from anki_pleco_importer.audio import (
    AudioGenerator,
    ForvoGenerator,
    AudioGeneratorFactory,
    MultiProviderAudioGenerator,
    TTSProviderNotAvailable,
    AudioGeneratorError,
)


class MockAudioGenerator(AudioGenerator):
    """Mock audio generator for testing."""

    def __init__(self, cache_dir=None, should_fail=False):
        super().__init__(cache_dir)
        self.should_fail = should_fail
        self.generated_files = []

    def is_available(self):
        return not self.should_fail

    def get_provider_name(self):
        return "mock"

    def generate_audio(self, text, output_file):
        if self.should_fail:
            return None

        # Create a mock audio file
        with open(output_file, "w") as f:
            f.write(f"mock audio for: {text}")

        self.generated_files.append(output_file)
        return output_file


class TestAudioGenerator:
    """Test base AudioGenerator functionality."""

    def test_cache_filename_generation(self):
        """Test cache filename generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = MockAudioGenerator(temp_dir)
            filename = generator._get_cache_filename("测试", "mock")

            assert filename.parent == Path(temp_dir)
            assert filename.name.startswith("mock_")
            assert filename.name.endswith(".mp3")

    def test_caching_behavior(self):
        """Test that caching works correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = MockAudioGenerator(temp_dir)

            # First generation should create file
            result1 = generator.generate_with_cache("测试")
            assert result1 is not None
            assert os.path.exists(result1)

            # Second generation should use cache
            result2 = generator.generate_with_cache("测试")
            assert result2 == result1
            assert len(generator.generated_files) == 1  # Only generated once

    def test_cache_miss(self):
        """Test cache miss behavior."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = MockAudioGenerator(temp_dir)

            # Check that file is not cached initially
            assert not generator._is_cached("测试", "mock")

            # Generate audio
            result = generator.generate_with_cache("测试")
            assert result is not None

            # Check that file is now cached
            assert generator._is_cached("测试", "mock")


class TestForvoGenerator:
    """Test Forvo API generator."""

    def test_availability_with_api_key(self):
        """Test availability when API key is provided."""
        generator = ForvoGenerator("test_api_key")
        assert generator.is_available()

        generator = ForvoGenerator("")
        assert not generator.is_available()

    @patch("requests.get")
    def test_successful_audio_download(self, mock_get):
        """Test successful audio download from Forvo."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = ForvoGenerator("test_api_key", temp_dir)
            output_file = os.path.join(temp_dir, "test.mp3")

            # Mock API response
            mock_response = Mock()
            mock_response.json.return_value = {"items": [{"pathmp3": "http://example.com/audio.mp3", "num_votes": 5}]}
            mock_response.raise_for_status.return_value = None

            # Mock audio download
            mock_audio_response = Mock()
            mock_audio_response.content = b"fake audio data"
            mock_audio_response.raise_for_status.return_value = None

            mock_get.side_effect = [mock_response, mock_audio_response]

            result = generator.generate_audio("测试", output_file)

            assert result == output_file
            assert os.path.exists(output_file)
            with open(output_file, "rb") as f:
                assert f.read() == b"fake audio data"

    @patch("requests.get")
    def test_no_pronunciation_found(self, mock_get):
        """Test behavior when no pronunciation is found."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = ForvoGenerator("test_api_key", temp_dir)
            output_file = os.path.join(temp_dir, "test.mp3")

            # Mock API response with no items
            mock_response = Mock()
            mock_response.json.return_value = {"items": []}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = generator.generate_audio("测试", output_file)
            assert result is None


class TestAudioGeneratorFactory:
    """Test AudioGeneratorFactory."""

    def test_create_forvo_generator(self):
        """Test creating Forvo generator."""
        config = {"api_key": "test_key"}
        generator = AudioGeneratorFactory.create_generator("forvo", config)
        assert isinstance(generator, ForvoGenerator)
        assert generator.api_key == "test_key"

    def test_create_unknown_provider(self):
        """Test creating unknown provider raises error."""
        with pytest.raises(ValueError, match="Unknown audio provider"):
            AudioGeneratorFactory.create_generator("unknown", {})

    def test_get_available_providers(self):
        """Test getting available providers."""
        config = {"forvo": {"api_key": "test_key"}, "azure": {}}  # Missing required config

        with patch.object(ForvoGenerator, "is_available", return_value=True):
            available = AudioGeneratorFactory.get_available_providers(config)
            assert "forvo" in available


class TestMultiProviderAudioGenerator:
    """Test MultiProviderAudioGenerator."""

    def test_provider_fallback(self):
        """Test that providers are tried in order until one succeeds."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mock generators
            failing_generator = MockAudioGenerator(temp_dir, should_fail=True)
            working_generator = MockAudioGenerator(temp_dir, should_fail=False)

            config = {"mock1": {}, "mock2": {}}

            multi_gen = MultiProviderAudioGenerator(["mock1", "mock2"], config, temp_dir)

            # Replace generators with our mocks
            multi_gen.generators = {"mock1": failing_generator, "mock2": working_generator}

            result = multi_gen.generate_audio("测试")

            # Should have used the working generator
            assert result is not None
            assert len(working_generator.generated_files) == 1

    def test_all_providers_fail(self):
        """Test behavior when all providers fail."""
        with tempfile.TemporaryDirectory() as temp_dir:
            failing_generator1 = MockAudioGenerator(temp_dir, should_fail=True)
            failing_generator2 = MockAudioGenerator(temp_dir, should_fail=True)

            config = {"mock1": {}, "mock2": {}}

            multi_gen = MultiProviderAudioGenerator(["mock1", "mock2"], config, temp_dir)

            # Replace generators with our mocks
            multi_gen.generators = {"mock1": failing_generator1, "mock2": failing_generator2}

            result = multi_gen.generate_audio("测试")
            assert result is None

    def test_get_available_providers(self):
        """Test getting list of available providers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            working_generator = MockAudioGenerator(temp_dir, should_fail=False)

            config = {"mock": {}}

            multi_gen = MultiProviderAudioGenerator(["mock"], config, temp_dir)
            multi_gen.generators = {"mock": working_generator}

            available = multi_gen.get_available_providers()
            assert available == ["mock"]


class TestErrorHandling:
    """Test error handling in audio generation."""

    def test_tts_provider_not_available_exception(self):
        """Test TTSProviderNotAvailable exception."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = MockAudioGenerator(temp_dir, should_fail=True)

            # Override to raise exception
            def failing_generate(text, output_file):
                raise TTSProviderNotAvailable("Provider not available")

            generator.generate_audio = failing_generate

            with pytest.raises(TTSProviderNotAvailable):
                generator.generate_audio("测试", "output.mp3")

    def test_audio_generator_error_inheritance(self):
        """Test that TTSProviderNotAvailable inherits from AudioGeneratorError."""
        assert issubclass(TTSProviderNotAvailable, AudioGeneratorError)

    def test_graceful_failure_in_multi_provider(self):
        """Test graceful failure handling in MultiProviderAudioGenerator."""
        with tempfile.TemporaryDirectory() as temp_dir:

            def exception_generator(text, output_file=None):
                raise Exception("Simulated failure")

            failing_generator = MockAudioGenerator(temp_dir)
            failing_generator.generate_with_cache = exception_generator

            working_generator = MockAudioGenerator(temp_dir, should_fail=False)

            config = {"failing": {}, "working": {}}

            multi_gen = MultiProviderAudioGenerator(["failing", "working"], config, temp_dir)
            multi_gen.generators = {"failing": failing_generator, "working": working_generator}

            # Should gracefully handle the exception and try the next provider
            result = multi_gen.generate_audio("测试")
            assert result is not None
            assert len(working_generator.generated_files) == 1
