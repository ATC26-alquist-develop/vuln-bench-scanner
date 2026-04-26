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
            
        # Check file permissions
        if not os.access(path, os.R_OK):
            print(f"Error: No read permission for {file_path}")
            return
            
        # Download file using shutil.copy2
        dest_path = path.with_suffix('.downloaded')
        shutil.copy2(path, dest_path)
        print(f"File downloaded to: {dest_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Secure file downloader')
    parser.add_argument('file_path', help='Path to the file to be downloaded')
    args = parser.parse_args()
    
    secure_download_file(args.file_path)

if __name__ == '__main__':
    main()