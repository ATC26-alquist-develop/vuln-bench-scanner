import os
import fnmatch
import sys

def find_and_delete_files(directory, pattern):
    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            file_path = os.path.join(root, filename)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python delete_files.py <directory> <pattern>")
        sys.exit(1)

    directory = sys.argv[1]
    pattern = sys.argv[2]

    find_and_delete_files(directory, pattern)