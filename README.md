## Initial Setup

### 1. Organize Playlist Songs:

- For each playlist, create a separate folder and place all the .flac files (songs) you want in that playlist into the folder.

### 2. Run the .m3u Creation Script:

- Use the [Python script](https://github.com/Vishwesh-Bhilare/music_tools/blob/main/extract_m3u.py) provided to generate an .m3u playlist file for each folder.
  
- Run the m3u extract script, example:
```py
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

### 3. Add the Folder Prefix to the .m3u Files:

- Place all .m3u files into a single folder (e.g., X:\music\Playlists).

- Use the [prefix-adding script](https://github.com/Vishwesh-Bhilare/music_tools/blob/main/add_prefix_to_m3u.py) to update the .m3u files to include the folder prefix All Songs/:
```py
import os

def add_folder_to_m3u(m3u_folder, new_folder_prefix):
    for file in os.listdir(m3u_folder):
        if file.endswith(".m3u"):
            m3u_path = os.path.join(m3u_folder, file)

            with open(m3u_path, "r", encoding="utf-8") as m3u_file:
                lines = m3u_file.readlines()

            updated_lines = [
                f"{new_folder_prefix}/{line.strip()}\n" for line in lines if line.strip()
            ]

            with open(m3u_path, "w", encoding="utf-8") as m3u_file:
                m3u_file.writelines(updated_lines)

m3u_folder = r"X:\music\Playlists"
new_folder_prefix = "All Songs"
add_folder_to_m3u(m3u_folder, new_folder_prefix)
```
### 4. Consolidate Songs:

- Move all .flac files from the individual playlist folders into a single All Songs folder.

- Ensure all files referenced in the .m3u files are now located in X:\music\All Songs.

### 5. Import .m3u Files into the Music Player:

- Copy both the All Songs folder and the .m3u files to your device if needed.

- Some players (e.g., Poweramp) require the .m3u files and the All Songs folder to be in the same relative location.
example structure: `X:\Music\All Songs, m3u files`

---

## Creating New Playlist

### 1. Download New Songs:
- Place the new songs into a temporary folder for the playlist.

### 2. Run the `.m3u` Creation Script:
- Use the script to generate an `.m3u` file for the new folder.

### 3. Add the Folder Prefix:
- Use the prefix-adding script to update the `.m3u` file by adding the `All Songs/` prefix.

### 4. Move Songs to `All Songs` Folder:
- Transfer the new songs from the temporary folder to the `All Songs` folder.

### 5. Import the Updated `.m3u` File:
- Ensure the `.m3u` file is in the same folder as the previous playlists and then import it into your music player.

---

## **Summary of Workflow**

- **For Existing Playlists:**
1. Put songs into separate folders.
2. Run the `.m3u` creation script for each folder.
3. Add the folder prefix to the `.m3u` files.
4. Move all songs to `All Songs`.
5. Import `.m3u` files into the music player.

- **For New Playlists:**
1. Download songs into a temporary folder.
2. Create an `.m3u` file for the folder.
3. Add the folder prefix to the `.m3u` file.
4. Move songs to `All Songs`.
5. Import the updated `.m3u` file.

