import os
import re
import sys

def secure_delete_file(file_path):
    """Securely delete a file by overwriting its contents before removal."""
    try:
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Overwrite file with random data
        with open(file_path, 'wb') as f:
            f.write(os.urandom(file_size))
        
        # Remove file
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")

def find_and_delete_files(directory, pattern):
    """Find and securely delete files matching the pattern in the given directory."""
    try:
        # Validate directory path
        directory = os.path.abspath(directory)
        if not os.path.isdir(directory):
            raise ValueError("Invalid directory path")

        # Validate pattern
        if not pattern or len(pattern) > 255:
            raise ValueError("Invalid pattern")

        # Compile regex pattern
        regex = re.compile(pattern)

        # Walk through directory
        for root, _, files in os.walk(directory):
            for file in files:
                if regex.search(file):
                    file_path = os.path.join(root, file)
                    secure_delete_file(file_path)
                    print(f"Deleted: {file_path}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <pattern>")
        sys.exit(1)

    directory = sys.argv[1]
    pattern = sys.argv[2]

    find_and_delete_files(directory, pattern)