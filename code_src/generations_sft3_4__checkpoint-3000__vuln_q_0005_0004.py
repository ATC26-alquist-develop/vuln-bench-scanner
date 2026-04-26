import os
import sys
import urllib.request
from pathlib import Path

def download_file(file_path):
    """
    Download a file from a given URL and save it to the current directory.
    
    Args:
        file_path (str): The URL or local path of the file to download
        
    Returns:
        None
    """
    try:
        # Convert to Path object for secure path handling
        path = Path(file_path).resolve()
        
        # Check if path is a file
        if not path.is_file():
            print("Error: Invalid file path")
            return
            
        # Check if file exists
        if not path.exists():
            print("Error: File does not exist")
            return
            
        # Create output directory if it doesn't exist
        output_dir = Path.cwd()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create output file path
        output_path = output_dir / path.name
        
        # Download file using urllib
        urllib.request.urlretrieve(str(path), str(output_path))
        print(f"File downloaded successfully to {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        download_file(sys.argv[1])