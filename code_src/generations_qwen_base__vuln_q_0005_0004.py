import sys
import requests

def download_file(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        file_name = url.split('/')[-1]  # Extract the file name from the URL
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded successfully as {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python download_file.py <file_url>")
        sys.exit(1)

    file_url = sys.argv[1]
    download_file(file_url)

if __name__ == "__main__":
    main()