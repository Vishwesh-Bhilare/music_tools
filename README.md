## Initial Setup

1. Organize Playlist Songs:

- For each playlist, create a separate folder and place all the .flac files (songs) you want in that playlist into the folder.

2. Run the .m3u Creation Script:

- Use the Python script provided to generate an .m3u playlist file for each folder.
- Run the m3u extract script, example:
```
import os

def create_m3u_playlist(music_directory):
    m3u_file_path = os.path.join(music_directory, "playlist.m3u")

    with open(m3u_file_path, "w") as m3u_file:
        for root, _, files in os.walk(music_directory):
            for file in files:
                if file.endswith(".flac"):
                    relative_path = os.path.relpath(os.path.join(root, file), music_directory)
                    m3u_file.write(relative_path + "\n")

music_directory = r"X:\music\PlaylistFolder"  # Replace with your folder path
create_m3u_playlist(music_directory)
```
- This creates an `.m3u` file that contains the relative paths of the songs in the folder.
