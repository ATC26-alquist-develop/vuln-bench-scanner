import requests
from urllib.parse import urlparse
import ssl
import certifi

def secure_https_connection(url: str, timeout: int = 10) -> requests.Response:
    """
    Establishes a secure HTTPS connection to a remote server.
    
    Args:
        url: The HTTPS URL to connect to
        timeout: Connection timeout in seconds
    
    Returns:
        requests.Response object containing the server response
    
    Raises:
        ValueError: If URL is not HTTPS
        requests.exceptions.RequestException: For connection errors
    """
    # Validate URL
    parsed_url = urlparse(url)
    if parsed_url.scheme != 'https':
        raise ValueError("URL must use HTTPS protocol")
    
    # Configure SSL context with high security settings
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.check_hostname = True
    
    try:
        # Make request with security settings
        response = requests.get(
            url,
            timeout=timeout,
            verify=True,
            cert=None,  # Disable certificate verification for self-signed certs
            allow_redirects=False,  # Prevent redirect attacks
            headers={'User-Agent': 'SecureClient/1.0'}
        )
        response.raise_for_status()
        return response
        
    except requests.exceptions.SSLError as e:
        raise requests.exceptions.RequestException(f"SSL Error: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Connection Error: {str(e)}")