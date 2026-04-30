import argparse
import os
import shutil
from pathlib import Path
import urllib.parse
import urllib.request

def validate_file_path(file_path: str) -> Path:
    """Validate and resolve the file path."""
    try:
        path = Path(file_path).resolve()
        if not path.is_file():
            raise ValueError("Invalid file path")
        return path
    except Exception as e:
        raise ValueError(f"Invalid file path: {str(e)}")

def download_file(url: str, destination: Path) -> None:
    """Download a file from a URL to a destination path."""
    try:
        # Validate URL
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme not in ('http', 'https'):
            raise ValueError("URL must use http or https scheme")

        # Download file
        with urllib.request.urlopen(url) as response:
            with open(destination, 'wb') as f:
                shutil.copyfileobj(response, f)
    except Exception as e:
        raise RuntimeError(f"Failed to download file: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Download a file from a URL")
    parser.add_argument("file_path", help="Path to the file to download")
    parser.add_argument("url", help="URL of the file to download")
    args = parser.parse_args()

    try:
        # Validate and resolve file path
        file_path = validate_file_path(args.file_path)

        # Validate URL
        parsed_url = urllib.parse.urlparse(args.url)
        if not parsed_url.scheme in ('http', 'https'):
            raise ValueError("URL must use http or https scheme")

        # Download file
        download_file(args.url, file_path)

        print(f"File downloaded successfully to {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()