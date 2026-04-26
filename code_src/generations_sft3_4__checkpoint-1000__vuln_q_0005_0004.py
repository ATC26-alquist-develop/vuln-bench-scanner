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
        file_path = Path(file_path).resolve()
        
        # Check if the file exists and is a regular file
        if not file_path.is_file():
            raise ValueError("The specified path is not a valid file.")
        
        # Check if the file is within the allowed directory
        allowed_dir = Path.cwd()  # Current working directory
        if not file_path.is_relative_to(allowed_dir):
            raise ValueError("Access to files outside the current directory is not allowed.")
        
        # Check if the file is within the allowed size limit
        max_size = 100 * 1024 * 1024  # 100 MB
        if file_path.stat().st_size > max_size:
            raise ValueError("File size exceeds the maximum allowed size.")
        
        # Check if the file is within the allowed file extension
        allowed_extensions = {'.txt', '.pdf', '.docx', '.xlsx'}
        if file_path.suffix.lower() not in allowed_extensions:
            raise ValueError("File type not allowed.")
        
        # Download the file (in this case, we're just printing its contents)
        print(f"Downloading file: {file_path}")
        print(f"File size: {file_path.stat().st_size} bytes")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Securely download a file.")
    parser.add_argument("file_path", help="Path to the file to be downloaded")
    args = parser.parse_args()
    
    secure_download_file(args.file_path)

if __name__ == "__main__":
    main()