"""Tests for Google Drive authentication functionality."""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile
import os

from anki_pleco_importer.google_drive import GoogleDriveClient, GoogleDriveError


class TestGoogleDriveAuth:
    """Test Google Drive authentication functionality."""

    def test_client_initialization(self):
        """Test GoogleDriveClient initialization with default values."""
        client = GoogleDriveClient()
        assert client.credentials_path == "credentials.json"
        assert client.token_path == "token.pickle"
        assert client.auto_open_browser is True
        assert client.host == "localhost"
        assert client.port == 0
        assert client.service is None

    def test_client_initialization_with_params(self):
        """Test GoogleDriveClient initialization with custom parameters."""
        client = GoogleDriveClient(
            credentials_path="custom_creds.json",
            token_path="custom_token.pickle",
            auto_open_browser=False,
            host="127.0.0.1",
            port=8080,
        )
        assert client.credentials_path == "custom_creds.json"
        assert client.token_path == "custom_token.pickle"
        assert client.auto_open_browser is False
        assert client.host == "127.0.0.1"
        assert client.port == 8080

    def test_get_auth_info_no_files(self):
        """Test get_auth_info when no files exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            client = GoogleDriveClient(
                credentials_path=f"{tmpdir}/creds.json",
                token_path=f"{tmpdir}/token.pickle",
            )

            auth_info = client.get_auth_info()

            assert auth_info["authenticated"] is False
            assert auth_info["token_file_exists"] is False
            assert auth_info["credentials_file_exists"] is False
            assert auth_info["token_path"] == f"{tmpdir}/token.pickle"
            assert auth_info["credentials_path"] == f"{tmpdir}/creds.json"

    def test_get_auth_info_with_token_file(self):
        """Test get_auth_info when token file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            token_path = f"{tmpdir}/token.pickle"

            # Create a dummy token file
            Path(token_path).write_text("dummy token")

            client = GoogleDriveClient(token_path=token_path)
            auth_info = client.get_auth_info()

            assert auth_info["token_file_exists"] is True
            assert "token_modified" in auth_info

    def test_clear_authentication(self):
        """Test clearing authentication tokens."""
        with tempfile.TemporaryDirectory() as tmpdir:
            token_path = f"{tmpdir}/token.pickle"

            # Create a dummy token file
            Path(token_path).write_text("dummy token")
            assert os.path.exists(token_path)

            client = GoogleDriveClient(token_path=token_path)
            client.service = Mock()  # Simulate authenticated state

            client.clear_authentication()

            assert not os.path.exists(token_path)
            assert client.service is None

    def test_is_authenticated(self):
        """Test authentication status checking."""
        client = GoogleDriveClient()

        # Initially not authenticated
        assert client.is_authenticated() is False

        # Simulate authenticated state
        client.service = Mock()
        assert client.is_authenticated() is True

    def test_authenticate_missing_credentials(self):
        """Test authentication fails when credentials file is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            client = GoogleDriveClient(credentials_path=f"{tmpdir}/missing_creds.json")

            with pytest.raises(GoogleDriveError) as exc_info:
                client.authenticate()

            assert "credentials file not found" in str(exc_info.value).lower()
            assert "console.cloud.google.com" in str(exc_info.value)

    @patch("anki_pleco_importer.google_drive.build")
    @patch("anki_pleco_importer.google_drive.InstalledAppFlow")
    def test_authenticate_oauth_flow(self, mock_flow_class, mock_build):
        """Test successful OAuth authentication flow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            creds_path = f"{tmpdir}/credentials.json"
            token_path = f"{tmpdir}/token.pickle"

            # Create dummy credentials file
            Path(creds_path).write_text('{"installed": {"client_id": "test"}}')

            # Mock the OAuth flow
            mock_flow = Mock()
            mock_flow_class.from_client_secrets_file.return_value = mock_flow
            mock_creds = Mock()
            mock_creds.valid = True
            mock_flow.run_local_server.return_value = mock_creds

            # Mock the Google API service
            mock_service = Mock()
            mock_build.return_value = mock_service

            client = GoogleDriveClient(
                credentials_path=creds_path,
                token_path=token_path,
                auto_open_browser=False,
            )

            client.authenticate(verbose=True)

            # Verify OAuth flow was called correctly
            mock_flow_class.from_client_secrets_file.assert_called_once_with(creds_path, client.SCOPES)
            mock_flow.run_local_server.assert_called_once_with(
                host="localhost",
                port=0,
                open_browser=False,
                success_message="✅ Authentication successful! You can close this tab and return to the terminal.",
                authorization_prompt_message="Please visit the following URL to authorize the application:\n{url}\n",
            )

            # Verify service was built
            mock_build.assert_called_once_with("drive", "v3", credentials=mock_creds)
            assert client.service == mock_service

    @patch("anki_pleco_importer.google_drive.pickle.load")
    @patch("anki_pleco_importer.google_drive.build")
    def test_authenticate_with_existing_valid_token(self, mock_build, mock_pickle_load):
        """Test authentication with existing valid token."""
        with tempfile.TemporaryDirectory() as tmpdir:
            token_path = f"{tmpdir}/token.pickle"

            # Create dummy token file
            Path(token_path).write_text("dummy token")

            # Mock valid credentials
            mock_creds = Mock()
            mock_creds.valid = True
            mock_pickle_load.return_value = mock_creds

            # Mock the Google API service
            mock_service = Mock()
            mock_build.return_value = mock_service

            client = GoogleDriveClient(token_path=token_path)
            client.authenticate()

            # Should use existing token without OAuth flow
            mock_build.assert_called_once_with("drive", "v3", credentials=mock_creds)
            assert client.service == mock_service

    @patch("anki_pleco_importer.google_drive.pickle.load")
    def test_authenticate_with_expired_token_refresh_success(self, mock_pickle_load):
        """Test authentication with expired token that can be refreshed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            token_path = f"{tmpdir}/token.pickle"

            # Create dummy token file
            Path(token_path).write_text("dummy token")

            # Mock expired but refreshable credentials
            mock_creds = Mock()
            mock_creds.valid = False
            mock_creds.expired = True
            mock_creds.refresh_token = "refresh_token"

            # Mock successful refresh
            def refresh_side_effect(request):
                mock_creds.valid = True

            mock_creds.refresh.side_effect = refresh_side_effect
            mock_pickle_load.return_value = mock_creds

            with patch("anki_pleco_importer.google_drive.build") as mock_build:
                mock_service = Mock()
                mock_build.return_value = mock_service

                client = GoogleDriveClient(token_path=token_path)
                client.authenticate(verbose=True)

                # Should refresh token
                mock_creds.refresh.assert_called_once()
                mock_build.assert_called_once_with("drive", "v3", credentials=mock_creds)
                assert client.service == mock_service
