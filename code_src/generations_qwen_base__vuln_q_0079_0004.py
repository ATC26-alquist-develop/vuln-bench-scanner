import os
import glob

def delete_files_matching_pattern(directory, pattern):
    """
    Deletes files in the specified directory that match the given pattern.

    :param directory: The directory to search for files.
    :param pattern: The file pattern to match (e.g., '*.txt').
    """
    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return

    # Construct the full pattern path
    full_pattern = os.path.join(directory, pattern)

    # Find all files that match the pattern
    matching_files = glob.glob(full_pattern)

    # Check if any files were found
    if not matching_files:
        print(f"No files matching the pattern {pattern} were found in {directory}.")
        return

    # Delete each matching file
    for file_path in matching_files:
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Failed to delete file {file_path}: {e}")

    print(f"Deleted {len(matching_files)} files matching the pattern {pattern} in {directory}.")

# Example usage
if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    pattern = input("Enter the file pattern to match (e.g., '*.txt'): ")
    delete_files_matching_pattern(directory, pattern)