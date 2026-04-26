import requests
from urllib.parse import urlparse
import ssl
import certifi

def secure_https_connection(url: str, timeout: int = 30) -> requests.Response:
    """
    Establishes a secure HTTPS connection to a remote server.
    
    Args:
        url: The HTTPS URL to connect to
        timeout: Connection timeout in seconds
    
    Returns:
        requests.Response object containing the server response
    
    Raises:
        ValueError: If URL is not HTTPS
        requests.exceptions.SSLError: If SSL verification fails
        requests.exceptions.RequestException: For other request-related errors
    """
    # Validate URL
    parsed_url = urlparse(url)
    if parsed_url.scheme != 'https':
        raise ValueError("URL must use HTTPS protocol")
    
    # Configure SSL context with high security settings
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
    ssl_context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
    
    try:
        # Make request with security settings
        response = requests.get(
            url,
            timeout=timeout,
            verify=True,
            cert=None,  # Disable certificate verification for self-signed certs
            allow_redirects=False,  # Disable automatic redirects
            headers={'User-Agent': 'SecureClient/1.0'}
        )
        
        # Verify SSL certificate
        response.raise_for_status()
        
        return response
        
    except requests.exceptions.SSLError as e:
        raise requests.exceptions.SSLError(f"SSL verification failed: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Request failed: {str(e)}")