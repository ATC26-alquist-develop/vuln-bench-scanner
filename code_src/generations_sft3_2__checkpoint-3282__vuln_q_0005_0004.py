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
            print("Error: The specified path is not a valid file.")
            return
        
        # Check if file is within allowed directory
        allowed_dir = Path.cwd()
        if not path.is_relative_to(allowed_dir):
            print("Error: Access to this file is not allowed.")
            return
            
        # Check if file is readable
        if not os.access(path, os.R_OK):
            print("Error: You don't have permission to read this file.")
            return
            
        # Download the file
        print(f"Downloading file: {path.name}")
        with open(path, 'rb') as source_file:
            with open(path.with_suffix('.downloaded'), 'wb') as dest_file:
                dest_file.write(source_file.read())
                
        print(f"File downloaded successfully as {path.with_suffix('.downloaded')}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Secure file downloader")
    parser.add_argument("file_path", help="Path to the file to be downloaded")
    args = parser.parse_args()
    
    secure_download_file(args.file_path)

if __name__ == "__main__":
    main()