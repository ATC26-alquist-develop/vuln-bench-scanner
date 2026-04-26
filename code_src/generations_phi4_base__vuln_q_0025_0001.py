import requests

def fetch_secure_content(url):
    """
    Establishes a secure connection to a remote server using HTTPS and retrieves the content.

    Parameters:
    url (str): The URL of the remote server to connect to.

    Returns:
    str: The content of the page at the given URL.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: Received status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Example usage
if __name__ == "__main__":
    url = "https://www.example.com"
    content = fetch_secure_content(url)
    print(content)