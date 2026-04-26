import os
import sys
import urllib.request
from pathlib import Path

def download_file(file_path):
    """
    Download a file from a given URL and save it to the current directory.
    
    Args:
        file_path (str): The URL or local path of the file to download.
    """
    try:
        # Resolve the path to its absolute form
        path = Path(file_path).resolve()
        
        # Check if the path is a file
        if not path.is_file():
            print("Error: The specified path is not a file.")
            return
            
        # Check if the file exists
        if not path.exists():
            print("Error: The file does not exist.")
            return
            
        # Create a temporary file to store the downloaded content
        temp_file = Path.cwd() / f"temp_{path.name}"
        
        # Download the file using urllib
        urllib.request.urlretrieve(str(path), str(temp_file))
        
        # Rename the temporary file to the original file name
        temp_file.rename(path)
        
        print(f"File downloaded successfully to {path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
        
    download_file(sys.argv[1])

if __name__ == "__main__":
    main()