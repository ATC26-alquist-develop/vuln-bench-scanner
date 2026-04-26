import os
import sys
import argparse
from pathlib import Path

def secure_download_file(file_path):
    """
    Securely download a file from the specified path.
    
    Args:
        file_path (str): The path to the file to be downloaded.
    """
    try:
        # Convert to absolute path and resolve any symlinks
        abs_path = os.path.abspath(os.path.realpath(file_path))
        
        # Check if the path exists and is a file
        if not os.path.isfile(abs_path):
            print(f"Error: {abs_path} is not a valid file.")
            return

        # Check if the file is within the allowed directory
        allowed_dir = os.path.abspath(os.getcwd())
        if not abs_path.startswith(allowed_dir):
            print(f"Error: Access to {abs_path} is not allowed.")
            return

        # Check if the file is within the allowed size limit
        max_size = 1024 * 1024 * 100  # 100 MB limit
        if os.path.getsize(abs_path) > max_size:
            print(f"Error: File size exceeds the maximum allowed size of {max_size} bytes.")
            return

        # Check if the file is readable
        if not os.access(abs_path, os.R_OK):
            print(f"Error: No read permission for {abs_path}.")
            return

        # Download the file
        with open(abs_path, 'rb') as source_file, open('downloaded_file', 'wb') as dest_file:
            dest_file.write(source_file.read())
        
        print(f"File downloaded successfully as 'downloaded_file'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Secure file downloader")
    parser.add_argument("file_path", help="Path to the file to be downloaded")
    args = parser.parse_args()

    secure_download_file(args.file_path)

if __name__ == "__main__":
    main()