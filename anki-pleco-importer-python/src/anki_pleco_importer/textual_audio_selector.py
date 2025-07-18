"""Textual-based audio selection interface for pronunciation choices."""

import tempfile
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, Callable, Iterator
import requests

from textual.app import App
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, ListItem, ListView
from textual.binding import Binding

logger = logging.getLogger(__name__)


class PronunciationItem:
    """Data class for pronunciation options."""

    def __init__(self, pronunciation_data: Dict[str, Any], is_skip: bool = False):
        self.pronunciation_data = pronunciation_data
        self.is_skip = is_skip
        self.username = pronunciation_data.get("username", "unknown") if not is_skip else "SKIP"
        self.sex = pronunciation_data.get("sex", "?") if not is_skip else ""
        self.country = pronunciation_data.get("country", "unknown") if not is_skip else ""
        self.votes = pronunciation_data.get("num_votes", 0) if not is_skip else 0
        self.rating = pronunciation_data.get("rate", 0) if not is_skip else 0
        self.audio_url = pronunciation_data.get("pathmp3", "") if not is_skip else ""

    def get_display_text(self) -> str:
        """Get formatted display text for this pronunciation."""
        if self.is_skip:
            return "⏭️  SKIP - Don't select any pronunciation"

        # Gender icons
        if self.sex == "f":
            gender_icon = "♀"  # Female
        elif self.sex == "m":
            gender_icon = "♂"  # Male
        else:
            gender_icon = "?"  # Unknown

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
        }

        country_display = country_flags.get(self.country, f"🏳️ {self.country}")
        stars = "⭐" * min(5, max(0, int(self.rating))) if self.rating > 0 else ""

        return (
            f"🎵 {self.username} ({gender_icon} {country_display}) - "
            f"{self.votes} votes, rating: {self.rating:.1f} {stars}"
        )


class AudioSelectorApp(App):
    """Textual app for selecting audio pronunciations."""

    CSS = """
    Screen {
        layout: vertical;
    }

    .container {
        height: 1fr;
        margin: 1;
    }

    ListView {
        height: 1fr;
        border: solid $primary;
        border-title-color: $secondary;
        border-title-style: bold;
    }

    .info-panel {
        height: 8;
        border: solid $accent;
        border-title-color: $accent;
        border-title-style: bold;
        padding: 1;
    }

    .selected-item {
        background: $primary;
        color: $text;
    }
    """

    BINDINGS = [
        Binding("up,k", "cursor_up", "Up", show=True),
        Binding("down,j", "cursor_down", "Down", show=True),
        Binding("enter", "select_item", "Select", show=True),
        Binding("space", "play_audio", "Play", show=True),
        Binding("s", "skip_all", "Skip", show=True),
        Binding("q,escape", "quit", "Quit", show=True),
    ]

    def __init__(
        self, text: str, pronunciations: List[Dict[str, Any]], play_audio_func: Callable[[str], bool], **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.pronunciations = pronunciations
        self.play_audio_func = play_audio_func
        self.selected_pronunciation: Optional[Dict[str, Any]] = None
        self.is_skipped = False
        self.pronunciation_items: List[PronunciationItem] = []
        self.preview_files: List[str] = []
        self.current_playing_file: Optional[str] = None

        # Create pronunciation items (skip option first)
        self.pronunciation_items.append(PronunciationItem({}, is_skip=True))
        for pronunciation in pronunciations:
            self.pronunciation_items.append(PronunciationItem(pronunciation))

    def compose(self) -> Iterator[Any]:
        """Create the app layout."""
        with Vertical(classes="container"):
            yield Header()
            yield Static(
                f"🎵 Select pronunciation for: [bold]{self.text}[/bold]\n"
                f"Found {len(self.pronunciations)} pronunciations",
                classes="info-panel",
            )

            # Create list view with pronunciation options
            list_items = []
            for item in self.pronunciation_items:
                list_items.append(ListItem(Static(item.get_display_text())))

            yield ListView(*list_items, classes="pronunciation-list")

            yield Static(
                "[bold]Controls:[/bold]\n"
                "↑/↓ or k/j: Navigate  |  Space: Play  |  Enter: Select  |  s: Skip  |  q/Esc: Quit",
                classes="info-panel",
            )
            yield Footer()

    def action_cursor_up(self) -> None:
        """Move cursor up in the list."""
        list_view = self.query_one(ListView)
        list_view.action_cursor_up()

    def action_cursor_down(self) -> None:
        """Move cursor down in the list."""
        list_view = self.query_one(ListView)
        list_view.action_cursor_down()

    def action_play_audio(self) -> None:
        """Play audio for currently selected item."""
        list_view = self.query_one(ListView)
        if list_view.index is not None:
            item = self.pronunciation_items[list_view.index]
            if not item.is_skip and item.audio_url:
                self._play_pronunciation_audio(item)

    def action_select_item(self) -> None:
        """Select the currently highlighted item."""
        list_view = self.query_one(ListView)
        if list_view.index is not None:
            item = self.pronunciation_items[list_view.index]
            if item.is_skip:
                self.is_skipped = True
                self.selected_pronunciation = None
            else:
                self.selected_pronunciation = item.pronunciation_data
            self.exit()

    def action_skip_all(self) -> None:
        """Skip all pronunciations."""
        self.is_skipped = True
        self.selected_pronunciation = None
        self.exit()

    def _play_pronunciation_audio(self, item: PronunciationItem) -> None:
        """Download and play audio for a pronunciation item."""
        if not item.audio_url:
            return

        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix=f"_{item.username}_{self.text[:10]}.mp3", delete=False)
            temp_file.close()

            # Update info panel to show download status
            info_panel = self.query_one(".info-panel")
            if isinstance(info_panel, Static):
                info_panel.update(
                    f"🎵 Select pronunciation for: [bold]{self.text}[/bold]\n"
                    f"🔊 Downloading and playing pronunciation by {item.username}..."
                )

            # Download audio
            logger.debug(f"Downloading preview audio from: {item.audio_url}")
            audio_response = requests.get(item.audio_url, timeout=30)
            audio_response.raise_for_status()

            with open(temp_file.name, "wb") as f:
                f.write(audio_response.content)

            # Track this file for cleanup
            self.preview_files.append(temp_file.name)
            self.current_playing_file = temp_file.name

            # Try to play the audio
            if self.play_audio_func(temp_file.name):
                if isinstance(info_panel, Static):
                    info_panel.update(
                        f"🎵 Select pronunciation for: [bold]{self.text}[/bold]\n"
                        f"✅ Played pronunciation by {item.username}"
                    )
            else:
                if isinstance(info_panel, Static):
                    info_panel.update(
                        f"🎵 Select pronunciation for: [bold]{self.text}[/bold]\n"
                        f"❌ Could not play audio (file downloaded but playback failed)"
                    )

        except Exception as e:
            # Update info panel with error
            info_panel = self.query_one(".info-panel")
            if isinstance(info_panel, Static):
                info_panel.update(
                    f"🎵 Select pronunciation for: [bold]{self.text}[/bold]\n" f"❌ Could not download audio: {str(e)}"
                )
            logger.warning(f"Failed to download/play audio: {e}")

    def on_exit(self) -> None:
        """Clean up when exiting the app."""
        self._cleanup_preview_files()

    def _cleanup_preview_files(self) -> None:
        """Clean up temporary preview files."""
        for file_path in self.preview_files:
            try:
                if Path(file_path).exists():
                    Path(file_path).unlink()
            except Exception as e:
                logger.warning(f"Failed to cleanup preview file {file_path}: {e}")


class TextualAudioSelector:
    """Textual-based audio selector for pronunciation choices."""

    def __init__(self, play_audio_func: Callable[[str], bool]):
        self.play_audio_func = play_audio_func

    def select_pronunciation(self, text: str, pronunciations: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Show audio selection interface and return selected pronunciation.

        Args:
            text: The Chinese text to select pronunciation for
            pronunciations: List of pronunciation dictionaries from Forvo API

        Returns:
            Selected pronunciation dictionary, or None if skipped
        """
        if not pronunciations:
            return None

        app = AudioSelectorApp(text=text, pronunciations=pronunciations, play_audio_func=self.play_audio_func)

        try:
            app.run()

            if app.is_skipped:
                logger.info(f"User skipped pronunciation selection for '{text}'")
                return None
            else:
                selected = app.selected_pronunciation
                if selected:
                    username = selected.get("username", "unknown")
                    logger.info(f"User selected pronunciation by '{username}' for '{text}'")
                return selected

        except KeyboardInterrupt:
            logger.info(f"User interrupted pronunciation selection for '{text}'")
            return None
        finally:
            # Ensure cleanup
            app._cleanup_preview_files()
