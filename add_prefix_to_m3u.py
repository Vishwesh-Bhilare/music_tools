import os

def add_folder_to_m3u(m3u_folder, new_folder_prefix):
    """Prepends a folder path to song names in all .m3u files in a directory.

    Args:
        m3u_folder: The folder containing the .m3u files.
        new_folder_prefix: The folder path to add before each song name.
    """
    for file in os.listdir(m3u_folder):
        if file.endswith(".m3u"):
            m3u_path = os.path.join(m3u_folder, file)
            
            # Read the .m3u file
            with open(m3u_path, "r", encoding="utf-8") as m3u_file:
                lines = m3u_file.readlines()
            
            # Update each line
            updated_lines = [
                f"{new_folder_prefix}/{line.strip()}\n" for line in lines if line.strip()
            ]
            
            # Write the updated lines back to the file
            with open(m3u_path, "w", encoding="utf-8") as m3u_file:
                m3u_file.writelines(updated_lines)
            
            print(f"Updated: {m3u_path}")


# Paths
m3u_folder = r"X:\music\Playlists"  # Folder containing your .m3u files
new_folder_prefix = "All Songs"  # Folder path to prepend

# Update the playlists
add_folder_to_m3u(m3u_folder, new_folder_prefix)
