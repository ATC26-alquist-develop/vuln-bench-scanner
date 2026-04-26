import requests
from requests.exceptions import RequestException

def establish_secure_connection(url):
    """
    Establishes a secure connection to a remote server using HTTPS.

    Args:
        url (str): The URL of the remote server.

    Returns:
        requests.Response: The response object from the server.

    Raises:
        RequestException: If there is an error during the request.
    """
    try:
        # Make the HTTPS request
        response = requests.get(url, verify=True)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        return response
    except RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
url = "https://example.com"
response = establish_secure_connection(url)

if response:
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")