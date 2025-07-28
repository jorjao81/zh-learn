#!/usr/bin/env python3
"""
Download comprehensive CJK fonts for Anki template use.
This script downloads BabelStone Han and Noto CJK fonts and prepares them for Anki.
"""

import os
import requests
import zipfile
from pathlib import Path
from urllib.parse import urlparse


def download_file(url: str, destination: Path, chunk_size: int = 8192) -> bool:
    """Download a file with progress indication."""
    try:
        print(f"Downloading {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get file size for progress tracking
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destination, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\rProgress: {progress:.1f}%", end='', flush=True)
        
        print(f"\n✓ Downloaded: {destination}")
        return True
        
    except Exception as e:
        print(f"\n✗ Failed to download {url}: {e}")
        return False


def extract_zip(zip_path: Path, extract_to: Path) -> bool:
    """Extract a ZIP file."""
    try:
        print(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✓ Extracted to: {extract_to}")
        return True
    except Exception as e:
        print(f"✗ Failed to extract {zip_path}: {e}")
        return False


def rename_for_anki(file_path: Path) -> Path:
    """Rename font file with underscore prefix for Anki."""
    new_name = f"_{file_path.name}"
    new_path = file_path.parent / new_name
    
    if file_path.exists():
        file_path.rename(new_path)
        print(f"✓ Renamed: {file_path.name} → {new_name}")
        return new_path
    else:
        print(f"✗ File not found: {file_path}")
        return file_path


def main():
    # Create fonts directory
    fonts_dir = Path(__file__).parent / "fonts"
    fonts_dir.mkdir(exist_ok=True)
    
    print("=== CJK Font Downloader for Anki Templates ===\n")
    
    # BabelStone Han (comprehensive CJK support)
    print("1. Downloading BabelStone Han...")
    babelstone_urls = [
        ("https://www.babelstone.co.uk/Fonts/Download/BabelStoneHan.zip", "BabelStoneHan.zip"),
        # Alternative direct links if ZIP not available
        ("https://www.babelstone.co.uk/Fonts/Download/BabelStoneHan.ttf", "BabelStoneHan.ttf"),
    ]
    
    for url, filename in babelstone_urls:
        dest_path = fonts_dir / filename
        if download_file(url, dest_path):
            if filename.endswith('.zip'):
                extract_zip(dest_path, fonts_dir)
                # Remove ZIP after extraction
                dest_path.unlink()
            break
    
    # Google Noto CJK Fonts
    print("\n2. Downloading Noto CJK Fonts...")
    noto_urls = [
        # Noto Sans CJK SC
        ("https://github.com/googlefonts/noto-cjk/raw/main/Sans/Variable/TTF/NotoSansCJKsc-VF.ttf", "NotoSansCJKsc.ttf"),
        # Noto Serif CJK SC  
        ("https://github.com/googlefonts/noto-cjk/raw/main/Serif/Variable/TTF/NotoSerifCJKsc-VF.ttf", "NotoSerifCJKsc.ttf"),
    ]
    
    for url, filename in noto_urls:
        dest_path = fonts_dir / filename
        download_file(url, dest_path)
    
    # HanaMin Fonts (Alternative comprehensive CJK support)
    print("\n3. Downloading HanaMin Fonts...")
    hanamin_urls = [
        # HanaMinA - BMP coverage
        ("https://github.com/cjkvi/HanaMinAFDKO/releases/download/8.030/HanaMinA.otf", "HanaMinA.otf"),
        # HanaMinB - Extension B coverage (most important for rare characters)
        ("https://github.com/cjkvi/HanaMinAFDKO/releases/download/8.030/HanaMinB.otf", "HanaMinB.otf"),
        # HanaMinC - Extensions C+ coverage
        ("https://github.com/cjkvi/HanaMinAFDKO/releases/download/8.030/HanaMinC.otf", "HanaMinC.otf"),
    ]
    
    for url, filename in hanamin_urls:
        dest_path = fonts_dir / filename
        download_file(url, dest_path)
    
    # Rename files for Anki (add underscore prefix)
    print("\n4. Preparing fonts for Anki...")
    font_files = list(fonts_dir.glob("*.ttf")) + list(fonts_dir.glob("*.woff*")) + list(fonts_dir.glob("*.otf"))
    
    anki_ready_fonts = []
    for font_file in font_files:
        if not font_file.name.startswith('_'):
            anki_font = rename_for_anki(font_file)
            anki_ready_fonts.append(anki_font)
    
    # Generate font usage instructions
    print("\n5. Generating installation instructions...")
    
    instructions = """# Font Installation Instructions

## Files Downloaded:
"""
    
    total_size = 0
    for font_file in anki_ready_fonts:
        if font_file.exists():
            size_mb = font_file.stat().st_size / (1024 * 1024)
            total_size += size_mb
            instructions += f"- {font_file.name} ({size_mb:.1f} MB)\n"
    
    instructions += f"\nTotal size: {total_size:.1f} MB\n\n"
    
    instructions += """## Installation Steps:

1. **Copy to Anki Media Folder:**
   Copy all _*.ttf files to your Anki media folder:
   - Windows: %APPDATA%\\Anki2\\[Profile]\\collection.media\\
   - macOS: ~/Library/Application Support/Anki2/[Profile]/collection.media/
   - Linux: ~/.local/share/Anki2/[Profile]/collection.media/

2. **Sync Collection:**
   Open Anki and sync to upload fonts to AnkiWeb

3. **Verify Installation:**
   Test with characters like 𦐇 in component analysis

## Alternative Installation:
Use the attach function in Anki to add font files to any note,
then reference them in card templates.
"""
    
    readme_path = fonts_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✓ Instructions saved to: {readme_path}")
    
    print(f"\n=== Download Complete ===")
    print(f"Fonts saved to: {fonts_dir}")
    print(f"Total files: {len(anki_ready_fonts)}")
    print(f"Total size: {total_size:.1f} MB")
    print(f"\nNext steps:")
    print(f"1. Copy files from {fonts_dir} to your Anki media folder")
    print(f"2. Sync your Anki collection")
    print(f"3. Test rare character display")


if __name__ == "__main__":
    main()