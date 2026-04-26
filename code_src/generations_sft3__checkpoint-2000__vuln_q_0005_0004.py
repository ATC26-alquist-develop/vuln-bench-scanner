import os
import sys
import argparse
from pathlib import Path
import requests
from urllib.parse import urlparse

def is_safe_path(base_path, path):
    """Check if the path is safe (within the base directory)"""
    return os.path.realpath(path).startswith(os.path.realpath(base_path))

def download_file(url):
    """Download file from URL and save it locally"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get the filename from the URL or content-disposition
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[-1].strip('"')
        else:
            filename = url.split('/')[-1]
            
        # Ensure the filename is safe
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(os.getcwd(), safe_filename)
        
        # Save the file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return file_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Download file from URL")
    parser.add_argument("url", help="URL of the file to download")
    args = parser.parse_args()

    # Validate URL
    parsed_url = urlparse(args.url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        print("Invalid URL format")
        sys.exit(1)

    # Get current working directory
    base_path = os.getcwd()
    
    # Download file
    file_path = download_file(args.url)
    
    if file_path:
        # Verify file was downloaded
        if not os.path.exists(file_path):
            print("File was not downloaded successfully")
            sys.exit(1)
        
        # Check if path is safe
        if not is_safe_path(base_path, file_path):
            print("Error: File path is not within the allowed directory")
            os.remove(file_path)
            sys.exit(1)
        
        print(f"File downloaded successfully to: {file_path}")
    else:
        print("File download failed")

if __name__ == "__main__":
    main()