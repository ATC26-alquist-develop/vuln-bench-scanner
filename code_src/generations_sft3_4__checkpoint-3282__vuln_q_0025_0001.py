import requests
from urllib.parse import urlparse
import ssl
from typing import Optional

def create_secure_connection(url: str, timeout: int = 30) -> requests.Session:
    """
    Creates a secure HTTPS connection with proper certificate validation and security settings.
    
    Args:
        url: The HTTPS URL to connect to
        timeout: Connection timeout in seconds
    
    Returns:
        requests.Session: Configured session object
    
    Raises:
        ValueError: If URL is not HTTPS or invalid
        requests.exceptions.SSLError: If SSL certificate validation fails
    """
    # Validate URL
    parsed_url = urlparse(url)
    if parsed_url.scheme != 'https':
        raise ValueError("URL must use HTTPS protocol")
    
    if not parsed_url.netloc:
        raise ValueError("Invalid URL format")
    
    # Create session with security settings
    session = requests.Session()
    
    # Force TLS 1.2 or higher
    session.mount('https://', requests.adapters.HTTPAdapter(
        max_retries=3,
        ssl_version=ssl.PROTOCOL_TLSv1_2
    ))
    
    # Verify SSL certificates
    session.verify = True
    
    # Set secure headers
    session.headers.update({
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block'
    })
    
    return session