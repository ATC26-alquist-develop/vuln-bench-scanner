import requests
from requests.exceptions import RequestException
import logging
from typing import Optional

def check_server_availability(url: str, timeout: int = 5) -> Optional[bool]:
    """
    Check if a server is available at the specified URL.
    
    Args:
        url (str): The URL of the server to check
        timeout (int): Timeout in seconds for the request (default: 5)
    
    Returns:
        Optional[bool]: True if server is available, False if not, None on error
    """
    try:
        # Make request with timeout
        response = requests.get(url, timeout=timeout)
        
        # Check status code
        if response.status_code == 200:
            return True
        else:
            logging.warning(f"Server returned status code {response.status_code}")
            return False
            
    except RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None

# ===== cell separator =====

if __name__ == "__main__":
    url = "https://example.com"
    result = check_server_availability(url)
    if result is True:
        print("Server is available")
    elif result is False:
        print("Server is not available")
    else:
        print("Failed to check server availability")