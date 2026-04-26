import os
import sys
import requests

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def main():
    if len(sys.argv) != 2:
        print("Usage: python download_file.py <file_url>")
        sys.exit(1)

    file_url = sys.argv[1]
    if not file_url.lower().startswith('http'):
        print("The URL must start with 'http' or 'https'.")
        sys.exit(1)

    local_filename = os.path.basename(file_url)
    try:
        download_file(file_url, local_filename)
        print(f"Downloaded '{local_filename}' successfully.")
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()