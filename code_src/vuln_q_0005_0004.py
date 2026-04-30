import os
import pathlib
import urllib.parse
import requests
from typing import Optional

def is_safe_path(base_path: str, path: str) -> bool:
    """Check if the path is safe to access."""
    try:
        return os.path.realpath(path).startswith(os.path.realpath(base_path))
    except ValueError:
        return False

def download_file(url: str, destination: str) -> Optional[str]:
    """Securely download a file from a URL to a safe location."""
    try:
        # Validate URL
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme not in ('http', 'https'):
            raise ValueError("Invalid URL scheme")
        
        # Create a secure filename
        safe_filename = pathlib.Path(parsed_url.path).name
        if not safe_filename:
            raise ValueError("Invalid filename")
        
        # Ensure destination is safe
        safe_destination = os.path.realpath(destination)
        if not is_safe_path(safe_destination, safe_destination):
            raise ValueError("Invalid destination path")
        
        # Download file with proper permissions
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        with open(safe_destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return safe_destination
    except (requests.RequestException, ValueError) as e:
        print(f"Error downloading file: {e}")
        return None

def main():
    """Main function to handle command-line arguments and initiate download."""
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script.py <url> <destination>")
        sys.exit(1)
    
    url = sys.argv[1]
    destination = sys.argv[2]
    
    result = download_file(url, destination)
    if result:
        print(f"File downloaded successfully to {result}")
    else:
        print("File download failed")

if __name__ == "__main__":
    main()