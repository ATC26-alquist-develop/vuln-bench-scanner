import argparse
import os
import urllib.parse
import urllib.request
import sys

def download_file(file_path: str) -> None:
    """
    Downloads a file from a given URL to the current working directory.
    
    Args:
        file_path: The URL of the file to download
    """
    # Validate and sanitize the file path
    try:
        parsed_url = urllib.parse.urlparse(file_path)
        if parsed_url.scheme not in ('http', 'https'):
            raise ValueError("Invalid URL scheme. Only HTTP and HTTPS are supported.")
        
        # Extract the filename from the URL
        filename = os.path.basename(parsed_url.path)
        if not filename:
            raise ValueError("Invalid filename extracted from URL.")
            
        # Create a safe filename
        safe_filename = os.path.basename(filename)
        if not safe_filename:
            raise ValueError("Invalid filename extracted from URL.")
            
        # Download the file
        with urllib.request.urlopen(file_path) as response:
            with open(safe_filename, 'wb') as f:
                f.write(response.read())
                
        print(f"File downloaded successfully: {safe_filename}")
        
    except Exception as e:
        print(f"Error downloading file: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Download a file from a URL')
    parser.add_argument('file_path', type=str, help='The URL of the file to download')
    args = parser.parse_args()
    
    download_file(args.file_path)

if __name__ == '__main__':
    main()