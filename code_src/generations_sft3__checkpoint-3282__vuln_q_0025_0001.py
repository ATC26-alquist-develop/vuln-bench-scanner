import requests
from urllib.parse import urlparse
import ssl
from typing import Optional

def create_secure_connection(url: str, timeout: int = 30) -> Optional[requests.Session]:
    """
    Establishes a secure HTTPS connection to a remote server.
    
    Args:
        url: The HTTPS URL to connect to
        timeout: Connection timeout in seconds
    
    Returns:
        requests.Session object or None if connection fails
    """
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL format")
        if parsed_url.scheme.lower() != "https":
            raise ValueError("URL must use HTTPS protocol")

        # Create session with security settings
        session = requests.Session()
        
        # Configure SSL context with secure defaults
        ssl_context = ssl.create_default_context()
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.check_hostname = True
        
        # Set secure headers
        session.headers.update({
            'User-Agent': 'SecureClient/1.0',
            'Accept': 'application/json',
        })

        # Make initial connection
        response = session.get(
            url,
            timeout=timeout,
            verify=True,  # Enforce SSL certificate verification
            allow_redirects=False  # Prevent redirect attacks
        )
        
        # Verify response
        response.raise_for_status()
        
        return session

    except (requests.exceptions.RequestException, ValueError) as e:
        # Log error here if needed
        return None