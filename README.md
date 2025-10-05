# 🎵 Music Organizer

A powerful, flexible music management tool that automatically organizes your local music collection, eliminates duplicates, and manages smart playlists based on metadata analysis. Perfect for music enthusiasts with large FLAC collections and curated playlists.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)


## 📁 Project Structure

```bash
.
├── music_organizer.py    # Main application
├── install.py           # Installation script
├── music_organizer_gui.py # GUI implementation
├── config/
│   └── music-organizer/
│       └── config.json  # User configuration
└── docs/
    ├── images/
    └── advanced-usage.md
```
---

## ✨ Features

### 🗂️ Automated File Organization
- **Smart File Moving**: Automatically moves music files from download directories to organized library structure
- **Duplicate Prevention**: Intelligent duplicate detection and handling with counter system
- **Multi-format Support**: Handles FLAC, MP3, WAV, M4A, AAC, and more
- **Safe File Operations**: Preserves file integrity with comprehensive error handling

### 📊 Metadata Intelligence
- **Advanced Metadata Parsing**: Extracts artist, title, album, genre, tempo, and year from audio files
- **Multi-format Metadata**: Supports FLAC, MP3, and other popular formats using Mutagen library
- **Filename Generation**: Customizable file naming conventions based on metadata

### 🎶 Smart Playlist Management
- **Automatic Playlist Assignment**: Adds files to playlists based on smart rules (genre, tempo, mood)
- **M3U Playlist Support**: Native support for standard M3U playlist format
- **Interactive Playlist Selection**: Choose playlists interactively or use automatic mode
- **Absolute Path References**: Creates reliable playlist entries with absolute file paths

### 🎛️ Flexible Configuration
- **First-Time Setup Wizard**: Guided configuration for new users
- **Customizable Directories**: Configurable source and destination directories
- **JSON Configuration**: Easy-to-edit configuration file for advanced users
- **Cross-Platform**: Works on Linux, Windows, and macOS

### 🖥️ Multiple Interfaces
- **Command-Line Interface**: Fast, scriptable CLI for power users and automation
- **Graphical User Interface**: User-friendly Tkinter GUI for casual users
- **i3wm Integration**: Native integration with i3 window manager

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/music-organizer.git
   cd music-organizer
   ```
   
2. Run the installer:
```bash
python install.py
```

3. First-time setup:
```bash
music-organizer --setup
```

### The installer will automatically:
- Install required Python dependencies (mutagen)
- Create a launcher script in your system PATH
- Set up default configuration in ~/.config/music-organizer/

### Basic Usage

- Organize music interactively:
  ```bash
  music-organizer
  ```

- Auto-mode (no prompts):
  ```bash
  music-organizer --auto
  ```
  
- Custom source directory:
  ```bash
  music-organizer --source ~/Downloads/music --auto
  ```
  
- Launch GUI:
  ```bash
  music-organizer --gui
  ```

### 📖 Detailed Usage
1. File Organization Process
  - Scanning: The tool scans all configured source directories for music files
  - Metadata Extraction: Reads ID3 tags and FLAC metadata from each file
  - File Moving: Moves files to Music/All Songs/ with organized filenames
  - Playlist Update: Adds file references to selected M3U playlists
  - Duplicate Handling: Automatically renames duplicates with counter

2. Smart Playlist Rules
  Configure smart playlists in config.json:

```jason
  "smart_playlists": {
    "High Energy.m3u": {"min_tempo": 120},
    "Chill.m3u": {"max_tempo": 90},
    "Rock.m3u": {"genre": ["rock", "alternative", "indie"]},
    "Jazz.m3u": {"genre": ["jazz", "blues", "swing"]}
  }
```

3. Configuration Options
| Setting            | Default            | Description                        |
|------------------------------------------------------------------------------| 
| music_root         | ~/Music            | Root music directory               |   
| all_songs_dir      | All Songs          | Directory for all organized files  |  
| source_dirs        | ["~/Downloads"]    | Directories to scan for new files  | 
| file_naming        | {artist} - {title} | Filename pattern                   | 
| supported_formats  | [".flac", ".mp3"]  | Supported audio formats            | 


### 🛠️ For Developers
Architecture Overview
The Music Organizer follows a modular architecture:

```bash
music_organizer/
├── core/
│   ├── organizer.py      # Main organization logic
│   ├── metadata.py       # Metadata extraction
│   └── playlists.py      # Playlist management
├── interfaces/
│   ├── cli.py           # Command-line interface
│   └── gui.py           # Graphical interface
└── config/
    ├── manager.py        # Configuration handling
    └── defaults.json     # Default settings
```

#### Extending Functionality

1. Adding New Audio Formats:
  ```python
  def parse_custom_metadata(file_path):
      # Add support for new formats
      pass
  ```

2. Creating Custom Playlist Rules:
  ```python
  def custom_playlist_rule(metadata):
      return metadata.get('bpm', 0) > 120 and 'electronic' in metadata.get('genre', '')
  ```

3. API Usage
  ```python
  from music_organizer import MusicOrganizer
  
  # Initialize organizer
  organizer = MusicOrganizer()

  # Organize specific directory
  organizer.organize_all(interactive=False, custom_source_dirs=['~/CustomMusic'])

  # Access metadata directly
  metadata = organizer.parse_audio_metadata(Path('song.flac'))
  ```


### 🤝 Contributing

We welcome contributions! Please see our Contributing Guide for details.
