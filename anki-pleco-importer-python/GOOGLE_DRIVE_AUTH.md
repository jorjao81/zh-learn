# Google Drive Authentication Guide

This document explains how to set up and use Google Drive authentication for downloading Pleco export files.

## Overview

The Anki Pleco Importer supports downloading your latest Pleco export files directly from Google Drive using OAuth2 authentication. This provides a seamless workflow where you can export from Pleco to Google Drive and then automatically download and process the files.

## Setup Instructions

### 1. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Drive API"
   - Click "Enable"

### 2. Create OAuth2 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type (unless you have a Google Workspace)
   - Fill in the required fields (App name, User support email, etc.)
   - Add your email to "Test users" if using External type
4. For Application type, select "Desktop application"
5. Give it a name (e.g., "Anki Pleco Importer")
6. Click "Create"

### 3. Download Credentials

1. After creating the OAuth client, click the download button (⬇️)
2. Save the file as `credentials.json` in your project directory
3. **Keep this file secure and never commit it to version control**

## Authentication Commands

### Check Authentication Status

```bash
anki-pleco-importer auth-status
```

This shows:
- Current authentication status
- Whether credentials and token files exist
- Setup instructions if needed

### Login (Authenticate)

```bash
# Standard authentication (opens browser automatically)
anki-pleco-importer auth-login

# With verbose output for troubleshooting
anki-pleco-importer auth-login --verbose

# Manual browser navigation (for remote/headless environments)
anki-pleco-importer auth-login --no-browser
```

#### First-time Authentication Flow

1. The command will open your default web browser
2. You'll be redirected to Google's OAuth consent screen
3. Sign in with your Google account
4. Grant permissions to access your Google Drive (read-only)
5. You'll see a success message
6. Return to the terminal - authentication is complete!

The authentication token is saved locally and will be automatically refreshed as needed.

### Logout (Clear Authentication)

```bash
anki-pleco-importer auth-logout
```

This removes stored authentication tokens, requiring you to re-authenticate next time.

## Using Google Drive Features

### Download Latest Flash File

```bash
# Download to current directory
anki-pleco-importer download-from-drive

# Download to specific directory
anki-pleco-importer download-from-drive --output-dir ~/Downloads

# With verbose output
anki-pleco-importer download-from-drive --verbose
```

This command:
- Searches your Google Drive for files starting with "flash-"
- Downloads the most recently created file
- Shows clear error messages if no files are found

## Authentication Details

### How It Works

1. **OAuth2 Flow**: Uses Google's standard OAuth2 flow for secure authentication
2. **Local Server**: Temporarily starts a local server to receive the OAuth callback
3. **Token Storage**: Saves refresh tokens locally for future use
4. **Auto-Refresh**: Automatically refreshes expired tokens
5. **Read-Only Access**: Only requests permission to read your Google Drive files

### Security Features

- **Minimal Permissions**: Only requests read-only access to Google Drive
- **Local Token Storage**: Tokens are stored locally in `token.pickle`
- **Automatic Refresh**: Expired tokens are refreshed automatically
- **No Password Storage**: Never stores your Google password

### Files Created

- `credentials.json`: OAuth2 client credentials (you provide this)
- `token.pickle`: Stored authentication tokens (auto-generated)

## Troubleshooting

### Common Issues

#### "Credentials file not found"
- Ensure `credentials.json` is in the current directory
- Verify the file was downloaded correctly from Google Cloud Console

#### "Authentication failed"
- Check that the Google Drive API is enabled in your project
- Verify OAuth2 credentials are configured for "Desktop application"
- Try running with `--verbose` for detailed error information

#### "Browser won't open"
- Use `--no-browser` flag and manually visit the displayed URL
- Check if you're in a remote/headless environment

#### "Permission denied" errors
- Ensure your OAuth consent screen is properly configured
- If using "External" user type, make sure your email is in "Test users"
- Check that the OAuth consent screen is published (if applicable)

### Headless/Remote Environments

For servers or environments without a display:

```bash
anki-pleco-importer auth-login --no-browser
```

This will display a URL that you can copy and paste into a browser on another machine.

### Re-authentication

If you encounter persistent authentication issues:

1. Clear existing authentication:
   ```bash
   anki-pleco-importer auth-logout
   ```

2. Check status:
   ```bash
   anki-pleco-importer auth-status
   ```

3. Re-authenticate:
   ```bash
   anki-pleco-importer auth-login --verbose
   ```

## Advanced Configuration

### Custom Credentials Location

You can specify custom paths for credentials and tokens:

```python
from anki_pleco_importer.google_drive import GoogleDriveClient

client = GoogleDriveClient(
    credentials_path="path/to/my-credentials.json",
    token_path="path/to/my-token.pickle"
)
```

### Custom OAuth Settings

```python
client = GoogleDriveClient(
    auto_open_browser=False,  # Don't auto-open browser
    host="127.0.0.1",        # Custom host for OAuth callback
    port=8080                # Custom port for OAuth callback
)
```

## Privacy and Data

- **No Data Collection**: This application doesn't collect or transmit your data
- **Local Processing**: All file processing happens locally on your machine
- **Read-Only Access**: Only reads files from your Google Drive
- **No File Modification**: Never modifies or deletes files in your Google Drive
- **Transparent**: All code is open source and auditable

## Need Help?

If you encounter issues:

1. Run commands with `--verbose` for detailed output
2. Check the authentication status: `anki-pleco-importer auth-status`
3. Verify your Google Cloud Console setup
4. Try re-authenticating: `auth-logout` then `auth-login`

The authentication system is designed to be robust and user-friendly while maintaining security best practices.
