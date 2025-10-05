#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
from pathlib import Path

def check_dependencies():
    """Check and install required dependencies"""
    required = ['mutagen']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("Installing missing dependencies...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run:")
            print(f"pip install {' '.join(missing)}")
            sys.exit(1)

def create_launcher_script():
    """Create a launcher script in PATH"""
    script_content = '''#!/bin/bash
python3 "{}" "$@"
'''.format(Path(__file__).resolve())
    
    # Try to install in /usr/local/bin (Linux/macOS)
    if platform.system() in ['Linux', 'Darwin']:
        launcher_path = Path('/usr/local/bin/music-organizer')
        try:
            launcher_path.write_text(script_content)
            launcher_path.chmod(0o755)
            print(f"✅ Launcher installed at {launcher_path}")
        except PermissionError:
            user_bin = Path.home() / '.local' / 'bin'
            user_bin.mkdir(parents=True, exist_ok=True)
            launcher_path = user_bin / 'music-organizer'
            launcher_path.write_text(script_content)
            launcher_path.chmod(0o755)
            print(f"✅ Launcher installed at {launcher_path}")
            print(f"📝 Add {user_bin} to your PATH if it's not already there")
    
    # Windows
    elif platform.system() == 'Windows':
        # Create batch file
        batch_content = f'@python "{Path(__file__).resolve()}" %*'
        launcher_path = Path.home() / 'AppData' / 'Local' / 'Microsoft' / 'WindowsApps' / 'music-organizer.bat'
        launcher_path.parent.mkdir(parents=True, exist_ok=True)
        launcher_path.write_text(batch_content)
        print(f"✅ Launcher installed at {launcher_path}")

def main():
    print("🎵 Music Organizer Installation")
    print("=" * 40)
    
    # Check dependencies
    check_dependencies()
    
    # Create launcher
    create_launcher_script()
    
    print("\n🎉 Installation complete!")
    print("\nQuick start:")
    print("1. Run 'music-organizer --setup' to configure")
    print("2. Run 'music-organizer' to organize your music")
    print("3. Use 'music-organizer --help' for more options")

if __name__ == "__main__":
    main()
