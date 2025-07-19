#!/usr/bin/env python3
"""
Quick test script to verify the audio selection interface behavior.
"""
import logging
from src.anki_pleco_importer.audio import ForvoGenerator

# Enable debug logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


def test_interactive_selection():
    """Test the interactive pronunciation selection."""

    # Mock pronunciation data
    mock_pronunciations = [
        {
            "username": "native_speaker_1",
            "sex": "f",
            "country": "China",
            "num_votes": 15,
            "rate": 4.5,
            "pathmp3": "https://example.com/audio1.mp3",
        },
        {
            "username": "native_speaker_2",
            "sex": "m",
            "country": "Taiwan",
            "num_votes": 8,
            "rate": 4.2,
            "pathmp3": "https://example.com/audio2.mp3",
        },
        {
            "username": "learner_voice",
            "sex": "f",
            "country": "United States",
            "num_votes": 3,
            "rate": 3.1,
            "pathmp3": "https://example.com/audio3.mp3",
        },
    ]

    # Create a ForvoGenerator (without real API key - just for testing interface)
    generator = ForvoGenerator(api_key="fake_key_for_testing", interactive_selection=True)

    print("Testing interactive pronunciation selection...")
    print("This should show an interface where audio plays when highlighting options")

    try:
        # Test the interactive selection
        result = generator._interactive_pronunciation_selection(mock_pronunciations, "你好")
        print(f"\nSelected result: {result}")

    except Exception as e:
        print(f"Error during test: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_interactive_selection()
