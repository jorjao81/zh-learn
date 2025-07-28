#!/usr/bin/env python3
"""
Install CJK fonts to Anki media folder for comprehensive character support.
"""

import os
import shutil
import platform
from pathlib import Path


def find_anki_media_folder():
    """Find the Anki media folder for the current user."""
    system = platform.system()
    home = Path.home()
    
    if system == "Windows":
        base_path = Path(os.environ.get('APPDATA', home / 'AppData/Roaming')) / 'Anki2'
    elif system == "Darwin":  # macOS
        base_path = home / 'Library/Application Support/Anki2'
    else:  # Linux and others
        base_path = home / '.local/share/Anki2'
    
    if not base_path.exists():
        return None
    
    # Find profile folders
    profiles = []
    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            media_folder = item / 'collection.media'
            if media_folder.exists():
                profiles.append((item.name, media_folder))
    
    return profiles


def copy_fonts(source_dir: Path, target_dir: Path):
    """Copy font files from source to target directory."""
    font_files = list(source_dir.glob('_*.ttf')) + list(source_dir.glob('_*.woff*')) + list(source_dir.glob('_*.otf'))
    
    if not font_files:
        print("❌ No font files found to copy")
        return False
    
    target_dir.mkdir(parents=True, exist_ok=True)
    
    copied_files = []
    total_size = 0
    
    for font_file in font_files:
        target_path = target_dir / font_file.name
        
        try:
            shutil.copy2(font_file, target_path)
            size_mb = font_file.stat().st_size / (1024 * 1024)
            total_size += size_mb
            copied_files.append((font_file.name, size_mb))
            print(f"✅ Copied: {font_file.name} ({size_mb:.1f} MB)")
        except Exception as e:
            print(f"❌ Failed to copy {font_file.name}: {e}")
            return False
    
    print(f"\n📁 Total: {len(copied_files)} files, {total_size:.1f} MB")
    return True


def main():
    print("=== Anki CJK Font Installer ===\n")
    
    # Find font files
    fonts_dir = Path(__file__).parent / "fonts"
    if not fonts_dir.exists():
        print("❌ Fonts directory not found. Run download_fonts.py first.")
        return
    
    # Find Anki profiles
    profiles = find_anki_media_folder()
    if not profiles:
        print("❌ No Anki installation found.")
        print("Please ensure Anki is installed and has been run at least once.")
        return
    
    print("📱 Found Anki profiles:")
    for i, (profile_name, media_folder) in enumerate(profiles, 1):
        print(f"  {i}. {profile_name} ({media_folder})")
    
    if len(profiles) == 1:
        choice = 1
        print(f"\n🎯 Auto-selecting profile: {profiles[0][0]}")
    else:
        try:
            choice = int(input(f"\nSelect profile (1-{len(profiles)}): "))
            if choice < 1 or choice > len(profiles):
                print("❌ Invalid choice")
                return
        except ValueError:
            print("❌ Invalid input")
            return
    
    profile_name, media_folder = profiles[choice - 1]
    
    print(f"\n📋 Installation Summary:")
    print(f"  Source: {fonts_dir}")
    print(f"  Target: {media_folder}")
    print(f"  Profile: {profile_name}")
    
    # List available fonts
    font_files = list(fonts_dir.glob('_*.ttf')) + list(fonts_dir.glob('_*.otf'))
    if font_files:
        print(f"\n📝 Fonts to install:")
        total_size = 0
        for font_file in font_files:
            size_mb = font_file.stat().st_size / (1024 * 1024)
            total_size += size_mb
            print(f"  • {font_file.name} ({size_mb:.1f} MB)")
        print(f"  Total size: {total_size:.1f} MB")
    
    confirm = input(f"\n❓ Install fonts to {profile_name}? (y/N): ").lower().strip()
    if confirm not in ['y', 'yes']:
        print("❌ Installation cancelled")
        return
    
    # Copy fonts
    print(f"\n🚀 Installing fonts...")
    if copy_fonts(fonts_dir, media_folder):
        print(f"\n✅ Installation completed successfully!")
        print(f"\n📝 Next steps:")
        print(f"  1. Open Anki")
        print(f"  2. Sync your collection to upload fonts")
        print(f"  3. Test rare character display (e.g., 𦐇)")
        print(f"\n💡 The fonts will now work across all your devices after syncing.")
    else:
        print(f"\n❌ Installation failed")


if __name__ == "__main__":
    main()