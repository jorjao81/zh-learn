"""Google Drive integration for downloading Pleco export files."""

import os
import pickle
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

logger = logging.getLogger(__name__)


class GoogleDriveError(Exception):
    """Custom exception for Google Drive related errors."""

    pass


class GoogleDriveClient:
    """Client for interacting with Google Drive API."""

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
    TOKEN_FILE = "token.pickle"
    CREDENTIALS_FILE = "credentials.json"

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
        auto_open_browser: bool = True,
        host: str = "localhost",
        port: int = 0,
    ):
        """Initialize the Google Drive client.

        Args:
            credentials_path: Path to OAuth2 credentials file
            token_path: Path to store authentication tokens
            auto_open_browser: Whether to automatically open browser for OAuth
            host: Host for OAuth callback server
            port: Port for OAuth callback server (0 for automatic)
        """
        self.credentials_path = credentials_path or self.CREDENTIALS_FILE
        self.token_path = token_path or self.TOKEN_FILE
        self.auto_open_browser = auto_open_browser
        self.host = host
        self.port = port
        self.service = None

    def authenticate(self, verbose: bool = False) -> None:
        """Authenticate with Google Drive API using OAuth2 browser flow.

        Args:
            verbose: Whether to show detailed authentication messages
        """
        creds = None

        # Load existing token
        if os.path.exists(self.token_path):
            try:
                with open(self.token_path, "rb") as token:
                    creds = pickle.load(token)
                    if verbose:
                        logger.info("Loaded existing authentication token")
            except Exception as e:
                logger.warning(f"Failed to load existing token: {e}")
                # Remove corrupted token file
                try:
                    os.remove(self.token_path)
                except Exception:
                    pass

        # If there are no valid credentials, request authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    if verbose:
                        logger.info("Refreshing expired authentication token")
                    creds.refresh(Request())
                    if verbose:
                        logger.info("Successfully refreshed authentication token")
                except Exception as e:
                    logger.warning(f"Failed to refresh token: {e}")
                    creds = None

            if not creds or not creds.valid:
                # Need to perform OAuth flow
                if not os.path.exists(self.credentials_path):
                    raise GoogleDriveError(
                        f"Google Drive credentials file not found: {self.credentials_path}\n\n"
                        "To set up Google Drive access:\n"
                        "1. Go to https://console.cloud.google.com/\n"
                        "2. Create a new project or select an existing one\n"
                        "3. Enable the Google Drive API\n"
                        "4. Create OAuth 2.0 credentials (Desktop application)\n"
                        "5. Download the credentials file as 'credentials.json'\n"
                        "6. Place it in the current directory"
                    )

                try:
                    if verbose:
                        logger.info("Starting OAuth2 authentication flow")

                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)

                    if verbose:
                        print("\n🔐 Google Drive Authentication Required")
                        print("=" * 50)
                        if self.auto_open_browser:
                            print("📱 Your web browser will open automatically for authentication")
                        else:
                            print("🌐 Please manually navigate to the URL that will be displayed")
                        print("🔒 You'll be asked to authorize access to your Google Drive")
                        print("📁 This app only requests read-only access to your files")
                        print("=" * 50)

                    # Run the OAuth flow
                    creds = flow.run_local_server(
                        host=self.host,
                        port=self.port,
                        open_browser=self.auto_open_browser,
                        success_message="✅ Authentication successful! "
                        "You can close this tab and return to the terminal.",
                        authorization_prompt_message=(
                            "Please visit the following URL to authorize the application:\n{url}\n"
                            if not self.auto_open_browser
                            else ""
                        ),
                    )

                    if verbose:
                        logger.info("✅ OAuth2 authentication completed successfully")

                except Exception as e:
                    raise GoogleDriveError(
                        f"Authentication failed: {e}\n\n"
                        "Common solutions:\n"
                        "• Ensure credentials.json is valid and in the current directory\n"
                        "• Check that the Google Drive API is enabled in your project\n"
                        "• Verify your OAuth2 credentials are configured for 'Desktop application'\n"
                        "• Try running with --verbose for more details"
                    )

            # Save the credentials for the next run
            try:
                with open(self.token_path, "wb") as token:
                    pickle.dump(creds, token)
                if verbose:
                    logger.info(f"Saved authentication token to {self.token_path}")
            except Exception as e:
                logger.warning(f"Failed to save token: {e}")

        try:
            self.service = build("drive", "v3", credentials=creds)
            if verbose:
                logger.info("🎯 Successfully connected to Google Drive API")
        except Exception as e:
            raise GoogleDriveError(f"Failed to build Google Drive service: {e}")

    def clear_authentication(self) -> None:
        """Clear stored authentication tokens to force re-authentication."""
        if os.path.exists(self.token_path):
            try:
                os.remove(self.token_path)
                logger.info("Cleared authentication token")
            except Exception as e:
                logger.warning(f"Failed to clear token: {e}")
        self.service = None

    def is_authenticated(self) -> bool:
        """Check if the client is currently authenticated."""
        return self.service is not None

    def get_auth_info(self) -> Dict[str, Any]:
        """Get information about current authentication status."""
        info = {
            "authenticated": self.is_authenticated(),
            "token_file_exists": os.path.exists(self.token_path),
            "credentials_file_exists": os.path.exists(self.credentials_path),
            "token_path": self.token_path,
            "credentials_path": self.credentials_path,
        }

        if info["token_file_exists"]:
            try:
                stat = os.stat(self.token_path)
                info["token_modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
            except Exception:
                pass

        return info

    def search_files(self, name_starts_with: str) -> List[Dict[str, Any]]:
        """Search for files in Google Drive that start with the given name."""
        if not self.service:
            raise GoogleDriveError("Not authenticated. Call authenticate() first.")

        query = f"name contains '{name_starts_with}' and trashed = false"

        try:
            results = (
                self.service.files()
                .list(q=query, fields="files(id, name, createdTime, modifiedTime)", orderBy="createdTime desc")
                .execute()
            )

            files = results.get("files", [])
            return files

        except Exception as e:
            raise GoogleDriveError(f"Failed to search files: {e}")

    def get_latest_flash_file(self) -> Optional[Dict[str, Any]]:
        """Get the most recently uploaded file starting with 'flash-'."""
        files = self.search_files("flash-")

        if not files:
            return None

        # Filter files that actually start with "flash-"
        flash_files = [f for f in files if f["name"].startswith("flash-")]

        if not flash_files:
            return None

        # Sort by creation time (most recent first)
        flash_files.sort(key=lambda f: datetime.fromisoformat(f["createdTime"].replace("Z", "+00:00")), reverse=True)

        return flash_files[0]

    def download_file(self, file_id: str, output_path: str) -> None:
        """Download a file from Google Drive."""
        if not self.service:
            raise GoogleDriveError("Not authenticated. Call authenticate() first.")

        try:
            request = self.service.files().get_media(fileId=file_id)
            file_io = io.BytesIO()
            downloader = MediaIoBaseDownload(file_io, request)

            done = False
            while done is False:
                status, done = downloader.next_chunk()

            # Write to file
            with open(output_path, "wb") as f:
                f.write(file_io.getvalue())

        except Exception as e:
            raise GoogleDriveError(f"Failed to download file: {e}")


def download_latest_flash_file(output_dir: str = ".", verbose: bool = False) -> str:
    """Download the latest flash file from Google Drive.

    Args:
        output_dir: Directory to save the downloaded file
        verbose: Whether to show detailed authentication messages

    Returns:
        Path to the downloaded file
    """
    client = GoogleDriveClient()
    client.authenticate(verbose=verbose)

    latest_file = client.get_latest_flash_file()
    if not latest_file:
        raise GoogleDriveError("No files starting with 'flash-' found in Google Drive")

    output_path = Path(output_dir) / latest_file["name"]
    client.download_file(latest_file["id"], str(output_path))

    return str(output_path)
