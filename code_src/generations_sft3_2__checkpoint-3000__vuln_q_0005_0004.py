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
        # Convert to Path object for secure path handling
        path = Path(file_path).resolve()
        
        # Check if path exists and is a file
        if not path.is_file():
            print(f"Error: {file_path} is not a valid file.")
            return
        
        # Check if file is within allowed directory
        allowed_dir = Path.cwd()
        if not path.is_relative_to(allowed_dir):
            print(f"Error: Access to {file_path} is not allowed.")
            return
        
        # Check file size (limit to 100MB)
        if path.stat().st_size > 100 * 1024 * 1024:
            print(f"Error: File size exceeds the limit of 100MB.")
            return
        
        # Download the file
        print(f"Downloading file: {path}")
        with open(path, 'rb') as source, open('downloaded_file', 'wb') as target:
            target.write(source.read())
        
        print("File downloaded successfully.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Secure file downloader")
    parser.add_argument("file_path", help="Path to the file to be downloaded")
    args = parser.parse_args()
    
    secure_download_file(args.file_path)

if __name__ == "__main__":
    main()