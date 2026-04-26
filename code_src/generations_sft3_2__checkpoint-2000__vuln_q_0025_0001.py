import ssl
import socket
from typing import Optional
from urllib.parse import urlparse

def create_secure_connection(url: str, timeout: int = 30) -> Optional[ssl.SSLSocket]:
    """
    Establishes a secure HTTPS connection to a remote server.
    
    Args:
        url: HTTPS URL to connect to
        timeout: Connection timeout in seconds
    
    Returns:
        SSLSocket object if connection successful, None if failed
    """
    try:
        # Parse URL
        parsed_url = urlparse(url)
        if parsed_url.scheme != 'https':
            raise ValueError("URL must use HTTPS protocol")

        # Create SSL context with secure defaults
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Create socket and wrap with SSL
        sock = socket.create_connection((parsed_url.hostname, parsed_url.port), timeout=timeout)
        secure_sock = context.wrap_socket(sock, server_hostname=parsed_url.hostname)

        return secure_sock

    except (socket.gaierror, socket.timeout, ssl.SSLError, ValueError) as e:
        # Log error here if needed
        return None