import requests
from urllib.parse import urlparse
import ssl

def secure_https_connection(url: str, timeout: int = 30) -> requests.Response:
    """
    Establishes a secure HTTPS connection to a remote server.
    
    Args:
        url: The HTTPS URL to connect to
        timeout: Connection timeout in seconds (default: 30)
    
    Returns:
        requests.Response object containing the response from the server
        
    Raises:
        ValueError: If the URL is not HTTPS or is invalid
        requests.exceptions.RequestException: If connection fails
    """
    # Validate URL
    parsed_url = urlparse(url)
    if parsed_url.scheme != 'https':
        raise ValueError('Only HTTPS URLs are supported')
    
    # Create session with secure defaults
    session = requests.Session()
    session.verify = True  # Force SSL verification
    
    try:
        # Make request with secure defaults
        response = session.get(
            url,
            timeout=timeout,
            verify=True,
            allow_redirects=False,  # Prevent redirect attacks
            headers={'User-Agent': 'SecureClient/1.0'}
        )
        response.raise_for_status()  # Raise exception for bad status codes
        return response
    except requests.exceptions.RequestException as e:
        raise
    finally:
        session.close()