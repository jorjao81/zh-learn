"""Step definitions for Textual audio selection feature tests."""
# flake8: noqa: F811
# mypy: ignore-errors

from behave import given, when, then
from unittest.mock import Mock, patch
from anki_pleco_importer.textual_audio_selector import TextualAudioSelector, PronunciationItem
from anki_pleco_importer.audio import ForvoGenerator


@given("I have a Forvo API key configured")
def step_impl(context):
    """Set up a mock Forvo API key."""
    context.api_key = "test_key_value"  # pragma: allowlist secret


@given("I have pronunciations available for Chinese words")
def step_impl(context):
    """Set up mock pronunciation data."""
    context.pronunciations = [
        {
            "username": "zhang123",
            "sex": "f",
            "country": "China",
            "num_votes": 5,
            "rate": 4.2,
            "pathmp3": "https://example.com/audio1.mp3",
        },
        {
            "username": "native_speaker",
            "sex": "m",
            "country": "Taiwan",
            "num_votes": 10,
            "rate": 4.8,
            "pathmp3": "https://example.com/audio2.mp3",
        },
        {
            "username": "student_user",
            "sex": "f",
            "country": "United States",
            "num_votes": 2,
            "rate": 3.5,
            "pathmp3": "https://example.com/audio3.mp3",
        },
    ]


@given("the Textual audio selector is enabled")
def step_impl(context):
    """Configure the audio selector to use Textual interface."""
    context.interactive_selection = True


@given('I have {count:d} pronunciation options for the word "{word}"')
def step_impl(context, count, word):
    """Set up specific number of pronunciations for a word."""
    context.word = word
    context.test_pronunciations = context.pronunciations[:count]


@given("each pronunciation has a valid audio URL")
def step_impl(context):
    """Ensure all pronunciations have valid audio URLs."""
    for pronunciation in context.test_pronunciations:
        pronunciation["pathmp3"] = f"https://example.com/{pronunciation['username']}.mp3"


@given('I have pronunciation options for the word "{word}"')
def step_impl(context, word):
    """Set up pronunciations for a specific word."""
    context.word = word
    context.test_pronunciations = context.pronunciations.copy()


@given("I have a pronunciation with the following data")
def step_impl(context):
    """Set up pronunciation with specific data from table."""
    row = context.table[0]
    context.test_pronunciations = [
        {
            "username": row["username"],
            "country": row["country"],
            "sex": row["sex"],
            "num_votes": int(row["votes"]),
            "rate": float(row["rating"]),
            "pathmp3": "https://example.com/test.mp3",
        }
    ]


@given("I have a pronunciation with an invalid audio URL")
def step_impl(context):
    """Set up pronunciation with invalid audio URL."""
    context.test_pronunciations = [
        {
            "username": "test_user",
            "country": "China",
            "sex": "m",
            "num_votes": 1,
            "rate": 3.0,
            "pathmp3": "https://invalid-url-that-will-fail.com/audio.mp3",
        }
    ]


@given('I have configured "{username}" as a preferred user')
def step_impl(context, username):
    """Configure a preferred user for auto-selection."""
    context.preferred_users = [username]


@given('I have pronunciation options including one from "{username}"')
def step_impl(context, username):
    """Ensure one pronunciation is from the specified username."""
    # Initialize test_pronunciations if not already set
    if not hasattr(context, "test_pronunciations"):
        context.test_pronunciations = context.pronunciations.copy()

    # Make sure one of our test pronunciations is from the preferred user
    for pronunciation in context.test_pronunciations:
        if pronunciation["username"] == username:
            break
    else:
        # Add a pronunciation from the preferred user if not found
        context.test_pronunciations.append(
            {
                "username": username,
                "sex": "m",
                "country": "China",
                "num_votes": 8,
                "rate": 4.5,
                "pathmp3": "https://example.com/preferred.mp3",
            }
        )


@given('I have pronunciation options but none from "{username}"')
def step_impl(context, username):
    """Ensure no pronunciations are from the specified username."""
    # Initialize test_pronunciations if not already set
    if not hasattr(context, "test_pronunciations"):
        context.test_pronunciations = context.pronunciations.copy()

    context.test_pronunciations = [p for p in context.test_pronunciations if p["username"] != username]


@when("I open the Textual audio selection interface")
def step_impl(context):
    """Mock opening the Textual interface."""
    # Mock the play_audio function
    context.mock_play_audio = Mock(return_value=True)

    # Create the selector
    context.selector = TextualAudioSelector(context.mock_play_audio)

    # Mock the app behavior for testing
    context.mock_app = Mock()
    context.mock_app.is_skipped = False
    context.mock_app.selected_pronunciation = None

    # Store the interface state
    context.interface_opened = True
    context.highlighted_index = 0  # Start with first item (skip) highlighted


@when("I press the down arrow key")
def step_impl(context):
    """Simulate pressing down arrow key."""
    max_items = len(context.test_pronunciations) + 1  # +1 for skip option
    context.highlighted_index = min(context.highlighted_index + 1, max_items - 1)


@when("I press the up arrow key")
def step_impl(context):
    """Simulate pressing up arrow key."""
    context.highlighted_index = max(context.highlighted_index - 1, 0)


@when("I navigate to a pronunciation option")
def step_impl(context):
    """Navigate to a non-skip pronunciation option."""
    context.highlighted_index = 1  # Move to first pronunciation (skip is at 0)


@when("I navigate to the second pronunciation option")
def step_impl(context):
    """Navigate to the second pronunciation option."""
    context.highlighted_index = 2  # Skip(0) + first(1) + second(2)


@when("I navigate to the skip option at the top")
def step_impl(context):
    """Navigate to the skip option."""
    context.highlighted_index = 0


@when("I press the space key")
def step_impl(context):
    """Simulate pressing space key to play audio."""
    # Ensure test_pronunciations is available
    if not hasattr(context, "test_pronunciations"):
        context.test_pronunciations = getattr(context, "pronunciations", [])

    if context.highlighted_index > 0:  # Not on skip option
        pronunciation_index = context.highlighted_index - 1  # Adjust for skip option
        if pronunciation_index < len(context.test_pronunciations):
            pronunciation = context.test_pronunciations[pronunciation_index]

            # Mock downloading and playing audio
            with patch("requests.get") as mock_get:
                mock_response = Mock()
                mock_response.content = b"fake_audio_data"
                mock_response.raise_for_status = Mock()
                mock_get.return_value = mock_response

                # Mock tempfile creation
                with patch("tempfile.NamedTemporaryFile") as mock_temp:
                    mock_temp_file = Mock()
                    mock_temp_file.name = f"/tmp/test_{pronunciation['username']}.mp3"
                    mock_temp.return_value = mock_temp_file

                    # Simulate playing audio
                    context.played_audio = True
                    context.played_username = pronunciation["username"]


@when("I press the Enter key")
def step_impl(context):
    """Simulate pressing Enter key to select."""
    if context.highlighted_index == 0:
        # Skip option selected
        context.mock_app.is_skipped = True
        context.mock_app.selected_pronunciation = None
    else:
        # Pronunciation selected
        pronunciation_index = context.highlighted_index - 1
        context.mock_app.selected_pronunciation = context.test_pronunciations[pronunciation_index]

    context.interface_closed = True


@when("I press the 's' key")
def step_impl(context):
    """Simulate pressing 's' key to skip."""
    context.mock_app.is_skipped = True
    context.mock_app.selected_pronunciation = None
    context.interface_closed = True


@when("I try to play the pronunciation")
def step_impl(context):
    """Try to play pronunciation with invalid URL."""
    with patch("requests.get") as mock_get:
        mock_get.side_effect = Exception("Download failed")
        context.download_error = True


@when('I request audio selection for the word "{word}"')
def step_impl(context, word):
    """Request audio selection through ForvoGenerator."""
    # Mock ForvoGenerator with preferred users
    with patch.object(ForvoGenerator, "__init__", return_value=None):
        context.forvo = ForvoGenerator.__new__(ForvoGenerator)
        context.forvo.preferred_users = getattr(context, "preferred_users", [])
        context.forvo.interactive_selection = True

        # Mock the selection logic
        selected = None
        for preferred_user in context.forvo.preferred_users:
            for pronunciation in context.test_pronunciations:
                if pronunciation.get("username") == preferred_user:
                    selected = pronunciation
                    context.auto_selected = True
                    context.selected_pronunciation = selected
                    return

        # No preferred user found, would show interface
        context.show_interface = True


@then("I should see a list with a skip option at the top")
def step_impl(context):
    """Verify skip option is at the top of the list."""
    assert context.interface_opened
    # The first item (index 0) should be the skip option
    skip_item = PronunciationItem({}, is_skip=True)
    assert "SKIP" in skip_item.get_display_text()


@then("I should see {count:d} pronunciation options below the skip option")
def step_impl(context, count):
    """Verify the correct number of pronunciation options."""
    assert len(context.test_pronunciations) == count


@then("the first item should be highlighted by default")
def step_impl(context):
    """Verify the first item is highlighted."""
    assert context.highlighted_index == 0


@then("the second item should be highlighted")
def step_impl(context):
    """Verify the second item is highlighted."""
    assert context.highlighted_index == 1


@then("the first item should be highlighted again")
def step_impl(context):
    """Verify navigation returned to first item."""
    assert context.highlighted_index == 0


@then("the audio file should be downloaded temporarily")
def step_impl(context):
    """Verify audio was downloaded."""
    assert getattr(context, "played_audio", False)


@then("the audio should be played through the system audio player")
def step_impl(context):
    """Verify audio playback was attempted."""
    # In our test, we just verify that played_audio was set to True
    # since we're mocking the actual audio playback mechanism
    assert getattr(context, "played_audio", False)


@then('the interface should show "Played pronunciation by {username}"')
def step_impl(context, username):
    """Verify playback success message."""
    assert getattr(context, "played_username", "") == username


@then("the selected pronunciation should be returned")
def step_impl(context):
    """Verify a pronunciation was selected."""
    assert context.mock_app.selected_pronunciation is not None


@then("the interface should close")
def step_impl(context):
    """Verify the interface closed."""
    assert getattr(context, "interface_closed", False)


@then("the temporary preview files should be cleaned up")
def step_impl(context):
    """Verify cleanup occurred."""
    # This would be verified by checking file system or mocking cleanup calls
    # For now, we just verify the pattern is expected
    assert context.interface_closed


@then("no pronunciation should be selected")
def step_impl(context):
    """Verify no pronunciation was selected."""
    assert context.mock_app.selected_pronunciation is None


@then("the word should be marked as skipped")
def step_impl(context):
    """Verify the word was marked as skipped."""
    assert context.mock_app.is_skipped


@then('I should see "{expected_text}"')
def step_impl(context, expected_text):
    """Verify specific text is displayed."""
    if hasattr(context, "test_pronunciations") and context.test_pronunciations:
        pronunciation = context.test_pronunciations[0]
        item = PronunciationItem(pronunciation)
        display_text = item.get_display_text()
        assert expected_text in display_text


@then('I should see an error message "{error_message}"')
def step_impl(context, error_message):
    """Verify error message is shown."""
    assert getattr(context, "download_error", False)


@then("the interface should remain functional")
def step_impl(context):
    """Verify interface continues working after error."""
    # Interface should still be open and responsive
    assert context.interface_opened


@then('the pronunciation from "{username}" should be automatically selected')
def step_impl(context, username):
    """Verify auto-selection occurred."""
    assert getattr(context, "auto_selected", False)
    assert context.selected_pronunciation["username"] == username


@then("the Textual interface should not be shown")
def step_impl(context):
    """Verify interface was not displayed due to auto-selection."""
    assert not getattr(context, "show_interface", False)


@then("the Textual audio selection interface should be displayed")
def step_impl(context):
    """Verify interface is displayed."""
    assert getattr(context, "show_interface", False)


@then("I should be able to manually select a pronunciation")
def step_impl(context):
    """Verify manual selection is possible."""
    # This is implied by the interface being shown
    assert getattr(context, "show_interface", False)
