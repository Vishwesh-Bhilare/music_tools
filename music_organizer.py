#!/usr/bin/env python3
import os
import shutil
import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
import subprocess

try:
    import mutagen
    from mutagen.flac import FLAC
    from mutagen.mp3 import MP3
    from mutagen import File
except ImportError:
    print("Error: Required dependencies not installed.")
    print("Please run: pip install mutagen")
    sys.exit(1)

class Config:
    """Configuration management for the music organizer"""
    
    DEFAULT_CONFIG = {
        "music_root": "~/Music",
        "all_songs_dir": "All Songs",
        "playlists_dir": ".",
        "source_dirs": ["~/Downloads", "~/Desktop"],
        "supported_formats": [".flac", ".mp3", ".wav", ".m4a", ".aac"],
        "smart_playlists": {
            "High Energy.m3u": {"min_tempo": 120},
            "Chill.m3u": {"max_tempo": 90},
            "Rock.m3u": {"genre": ["rock", "alternative", "indie"]},
            "Jazz.m3u": {"genre": ["jazz", "blues", "swing"]},
            "Classical.m3u": {"genre": ["classical", "orchestral", "symphony"]},
            "Electronic.m3u": {"genre": ["electronic", "edm", "dubstep", "house", "techno"]},
            "Hip-Hop.m3u": {"genre": ["hip-hop", "rap", "trap"]}
        },
        "file_naming": "{artist} - {title}",
        "auto_import": False,
        "backup_playlists": True
    }
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "music-organizer"
        self.config_file = self.config_dir / "config.json"
        self.data = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration, creating default if needed"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.data = json.load(f)
                print(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                self.data = self.DEFAULT_CONFIG.copy()
        else:
            self.data = self.DEFAULT_CONFIG.copy()
            self.save_config()
            print(f"Created default configuration at {self.config_file}")
        
        # Ensure all default keys exist
        for key, value in self.DEFAULT_CONFIG.items():
            if key not in self.data:
                self.data[key] = value
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_path(self, key, default=None):
        """Get a path from config and expand user directory"""
        path = self.data.get(key, default)
        if path:
            return Path(path).expanduser()
        return None
    
    def update_setting(self, key, value):
        """Update a configuration setting"""
        self.data[key] = value
        return self.save_config()

class MusicOrganizer:
    def __init__(self):
        self.config = Config()
        self.setup_paths()
    
    def setup_paths(self):
        """Setup directory paths from configuration"""
        self.music_root = self.config.get_path("music_root")
        self.all_songs_dir = self.music_root / self.config.data.get("all_songs_dir", "All Songs")
        self.playlists_dir = self.music_root / self.config.data.get("playlists_dir", ".")
        
        # Create directories if they don't exist
        self.all_songs_dir.mkdir(parents=True, exist_ok=True)
        self.playlists_dir.mkdir(parents=True, exist_ok=True)
    
    def parse_audio_metadata(self, file_path: Path) -> Dict:
        """Extract metadata from various audio formats"""
        try:
            audio = File(file_path)
            if audio is None:
                return self._get_fallback_metadata(file_path)
            
            metadata = {
                'title': self._get_tag(audio, 'title', file_path.stem),
                'artist': self._get_tag(audio, 'artist', 'Unknown Artist'),
                'album': self._get_tag(audio, 'album', 'Unknown Album'),
                'genre': self._get_tag(audio, 'genre', 'Unknown'),
                'tempo': self._parse_tempo(self._get_tag(audio, 'bpm', '0')),
                'date': self._get_tag(audio, 'date', ''),
                'tracknumber': self._get_tag(audio, 'tracknumber', ''),
                'file_path': file_path
            }
            
            return metadata
            
        except Exception as e:
            print(f"Error reading metadata from {file_path}: {e}")
            return self._get_fallback_metadata(file_path)
    
    def _get_tag(self, audio, tag, default):
        """Safely get tag from audio file"""
        try:
            if hasattr(audio, 'tags') and audio.tags is not None:
                if tag in audio.tags:
                    value = audio.tags[tag]
                    if isinstance(value, list):
                        return str(value[0])
                    return str(value)
        except:
            pass
        return default
    
    def _parse_tempo(self, tempo_str):
        """Parse tempo string to integer"""
        try:
            return int(float(tempo_str))
        except:
            return 0
    
    def _get_fallback_metadata(self, file_path):
        """Get basic metadata when file parsing fails"""
        return {
            'title': file_path.stem,
            'artist': 'Unknown Artist',
            'album': 'Unknown Album',
            'genre': 'Unknown',
            'tempo': 0,
            'date': '',
            'tracknumber': '',
            'file_path': file_path
        }
    
    def find_music_files(self, custom_source_dirs: List[str] = None) -> List[Path]:
        """Find music files in source directories"""
        source_dirs = custom_source_dirs or self.config.data.get('source_dirs', [])
        supported_formats = self.config.data.get('supported_formats', ['.flac', '.mp3'])
        
        music_files = []
        for source_dir in source_dirs:
            source_path = Path(source_dir).expanduser()
            if not source_path.exists():
                print(f"Warning: Source directory {source_path} does not exist")
                continue
                
            for ext in supported_formats:
                try:
                    music_files.extend(source_path.rglob(f"*{ext}"))
                    music_files.extend(source_path.rglob(f"*{ext.upper()}"))
                except Exception as e:
                    print(f"Error scanning {source_path} for {ext}: {e}")
        
        return music_files
    
    def generate_filename(self, metadata: Dict) -> str:
        """Generate filename based on naming pattern"""
        pattern = self.config.data.get('file_naming', '{artist} - {title}')
        
        # Clean components for filename safety
        artist = self._clean_filename(metadata['artist'])
        title = self._clean_filename(metadata['title'])
        album = self._clean_filename(metadata['album'])
        
        filename = pattern.format(
            artist=artist,
            title=title,
            album=album,
            genre=metadata['genre'],
            track=metadata['tracknumber']
        )
        
        # Add file extension
        file_path = metadata['file_path']
        return f"{filename}{file_path.suffix}"
    
    def _clean_filename(self, name):
        """Clean string for use in filename"""
        if not name:
            return "Unknown"
        
        # Remove or replace problematic characters
        cleaned = "".join(c for c in name if c not in '<>:"/\\|?*')
        cleaned = cleaned.replace('\n', ' ').replace('\r', ' ')
        cleaned = cleaned.strip()
        
        return cleaned if cleaned else "Unknown"
    
    def organize_file(self, file_path: Path, interactive: bool = True) -> bool:
        """Move and organize a single music file"""
        try:
            metadata = self.parse_audio_metadata(file_path)
            new_filename = self.generate_filename(metadata)
            dest_path = self.all_songs_dir / new_filename
            
            # Handle duplicate files
            dest_path = self._handle_duplicates(dest_path)
            
            # Move file
            shutil.move(str(file_path), str(dest_path))
            print(f"✓ Moved: {file_path.name} → {dest_path.name}")
            
            # Update playlists
            if interactive:
                self.update_playlists_interactive(dest_path, metadata)
            else:
                self.update_smart_playlists(dest_path, metadata)
            
            return True
            
        except Exception as e:
            print(f"✗ Error organizing {file_path}: {e}")
            return False
    
    def _handle_duplicates(self, dest_path: Path) -> Path:
        """Handle duplicate filenames by adding counter"""
        if not dest_path.exists():
            return dest_path
        
        counter = 1
        original_stem = dest_path.stem
        original_suffix = dest_path.suffix
        
        while dest_path.exists():
            dest_path = dest_path.parent / f"{original_stem} ({counter}){original_suffix}"
            counter += 1
        
        return dest_path
    
    def get_available_playlists(self) -> List[Path]:
        """Get list of all .m3u files in playlists directory"""
        return list(self.playlists_dir.glob("*.m3u"))
    
    def update_playlists_interactive(self, file_path: Path, metadata: Dict):
        """Interactively add file to playlists"""
        playlists = self.get_available_playlists()
        
        if not playlists:
            print("No playlists found. Create some .m3u files in your playlists directory.")
            if input("Create sample playlists? (y/N): ").lower() == 'y':
                self.create_sample_playlists()
                playlists = self.get_available_playlists()
            else:
                return
        
        print(f"\n🎵 Organized: {metadata['artist']} - {metadata['title']}")
        print("Available playlists:")
        for i, playlist in enumerate(playlists, 1):
            print(f"  {i}. {playlist.name}")
        print("  a. Add to all smart playlists automatically")
        print("  n. Don't add to any playlists")
        
        choice = input("\nSelect playlists (comma-separated numbers, 'a' for auto, 'n' for none): ").strip().lower()
        
        if choice == 'a':
            self.update_smart_playlists(file_path, metadata)
        elif choice == 'n':
            return
        elif choice:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                for idx in indices:
                    if 0 <= idx < len(playlists):
                        self.add_to_playlist(playlists[idx], file_path)
            except ValueError:
                print("Invalid input. Skipping playlist updates.")
    
    def update_smart_playlists(self, file_path: Path, metadata: Dict):
        """Automatically add to smart playlists based on metadata"""
        smart_playlists = self.config.data.get('smart_playlists', {})
        added_to = []
        
        for playlist_name, rules in smart_playlists.items():
            playlist_path = self.playlists_dir / playlist_name
            if self.matches_rules(metadata, rules):
                self.add_to_playlist(playlist_path, file_path)
                added_to.append(playlist_name)
        
        if added_to:
            print(f"  Automatically added to: {', '.join(added_to)}")
    
    def matches_rules(self, metadata: Dict, rules: Dict) -> bool:
        """Check if metadata matches smart playlist rules"""
        for key, value in rules.items():
            if key == 'min_tempo' and metadata.get('tempo', 0) < value:
                return False
            if key == 'max_tempo' and metadata.get('tempo', 0) > value:
                return False
            if key == 'genre':
                # Handle both string and list of genres
                if isinstance(value, list):
                    if not any(genre.lower() in metadata.get('genre', '').lower() for genre in value):
                        return False
                elif value.lower() not in metadata.get('genre', '').lower():
                    return False
        return True
    
    def add_to_playlist(self, playlist_path: Path, file_path: Path):
        """Add file path to playlist"""
        abs_path = file_path.resolve()
        
        # Create playlist if it doesn't exist
        playlist_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if already in playlist
        if playlist_path.exists():
            with open(playlist_path, 'r', encoding='utf-8') as f:
                existing_entries = [line.strip() for line in f.readlines()]
            
            if str(abs_path) in existing_entries:
                return  # Already exists
        
        # Add to playlist
        with open(playlist_path, 'a', encoding='utf-8') as f:
            f.write(f"{abs_path}\n")
    
    def create_sample_playlists(self):
        """Create sample playlists based on configuration"""
        smart_playlists = self.config.data.get('smart_playlists', {})
        
        for playlist_name in smart_playlists.keys():
            playlist_path = self.playlists_dir / playlist_name
            playlist_path.touch()
            print(f"  Created: {playlist_name}")
    
    def organize_all(self, interactive: bool = True, custom_source_dirs: List[str] = None):
        """Organize all music files found in source directories"""
        music_files = self.find_music_files(custom_source_dirs)
        
        if not music_files:
            print("No music files found in source directories.")
            print(f"Current source directories: {self.config.data['source_dirs']}")
            print(f"Supported formats: {self.config.data['supported_formats']}")
            return
        
        print(f"Found {len(music_files)} music file(s) to organize:")
        for file_path in music_files:
            print(f"  - {file_path}")
        
        if interactive and len(music_files) > 0:
            response = input("\nProceed with organization? (Y/n): ").strip().lower()
            if response in ['n', 'no']:
                return
        
        success_count = 0
        for file_path in music_files:
            if self.organize_file(file_path, interactive):
                success_count += 1
        
        print(f"\n🎉 Organization complete! {success_count}/{len(music_files)} files processed.")
    
    def show_config(self):
        """Display current configuration"""
        print("\nCurrent Configuration:")
        print(f"Music root: {self.music_root}")
        print(f"All songs directory: {self.all_songs_dir}")
        print(f"Playlists directory: {self.playlists_dir}")
        print(f"Source directories: {self.config.data['source_dirs']}")
        print(f"Supported formats: {self.config.data['supported_formats']}")
        print(f"Smart playlists: {list(self.config.data.get('smart_playlists', {}).keys())}")

def setup_wizard():
    """Interactive setup wizard for first-time users"""
    print("🎵 Music Organizer Setup Wizard")
    print("=" * 40)
    
    config = Config()
    
    print("\nLet's configure your music organizer...")
    
    # Music root directory
    current_music = config.data['music_root']
    new_music = input(f"Music root directory [{current_music}]: ").strip()
    if new_music:
        config.data['music_root'] = new_music
    
    # All songs directory
    current_all_songs = config.data['all_songs_dir']
    new_all_songs = input(f"All songs directory (within music root) [{current_all_songs}]: ").strip()
    if new_all_songs:
        config.data['all_songs_dir'] = new_all_songs
    
    # Source directories
    print(f"\nCurrent source directories: {config.data['source_dirs']}")
    print("Enter additional source directories (one per line, empty to finish):")
    while True:
        source_dir = input("> ").strip()
        if not source_dir:
            break
        if source_dir not in config.data['source_dirs']:
            config.data['source_dirs'].append(source_dir)
    
    config.save_config()
    print("\n✅ Setup complete! Configuration saved.")
    return MusicOrganizer()

def main():
    parser = argparse.ArgumentParser(
        description='Music Organizer - Organize your music files and playlists',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  music-organizer                    # Interactive organization
  music-organizer --auto            # Non-interactive mode
  music-organizer --source ~/Music/New  # Custom source directory
  music-organizer --config          # Show current configuration
  music-organizer --setup           # Run setup wizard
  music-organizer --gui             # Launch GUI (if available)
        '''
    )
    
    parser.add_argument('--auto', action='store_true', 
                       help='Non-interactive mode')
    parser.add_argument('--source', '-s', action='append',
                       help='Custom source directory (can be used multiple times)')
    parser.add_argument('--config', action='store_true',
                       help='Show current configuration')
    parser.add_argument('--setup', action='store_true',
                       help='Run setup wizard')
    parser.add_argument('--gui', action='store_true',
                       help='Launch GUI interface')
    
    args = parser.parse_args()
    
    # Setup wizard
    if args.setup:
        organizer = setup_wizard()
        return
    
    organizer = MusicOrganizer()
    
    # Show configuration
    if args.config:
        organizer.show_config()
        return
    
    # GUI mode
    if args.gui:
        try:
            from music_organizer_gui import launch_gui
            launch_gui(organizer)
            return
        except ImportError:
            print("GUI not available. Using CLI mode.")
    
    # Organize music
    organizer.organize_all(
        interactive=not args.auto,
        custom_source_dirs=args.source
    )

if __name__ == "__main__":
    main()
