import os

# Specify the directory you want to list
directory_path = 'C:\\Users\\Daveberry\\Documents\\Noteted Test'

try:
    # Get the list of all files and directories
    entries = os.listdir(directory_path)
    for entry in entries:
        print(entry)
except FileNotFoundError:
    print(f"The directory '{directory_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")