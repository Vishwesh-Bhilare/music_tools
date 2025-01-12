import os

def create_m3u_playlist(music_directory):
    """Creates an M3U playlist for all .flac files in a given directory.

    Args:
        music_directory: The path to the root music directory.
    """

    m3u_file_path = os.path.join(music_directory, "music_playlist.m3u")

    with open(m3u_file_path, "w") as m3u_file:
        for root, _, files in os.walk(music_directory):
            for file in files:
                if file.endswith(".flac"):
                    relative_path = os.path.relpath(os.path.join(root, file), music_directory)
                    m3u_file.write(relative_path + "\n")

# Replace 'X:\Music' with the actual path to your music directory
# Create separate m3u files for each playlist
music_directory = r"X:\Music"
create_m3u_playlist(music_directory)
