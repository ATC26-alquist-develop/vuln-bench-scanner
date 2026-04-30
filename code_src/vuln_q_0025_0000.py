```python
import ssl
import socket
import certifi
from urllib.parse import urlparse
import logging
from typing import Optional

def is_ssl_certificate_valid(url: str, timeout: int = 5) -> Optional[bool]:
    """
    Securely check SSL certificate validity of a website.
    
    Args:
        url: The website URL to check
        timeout: Connection timeout in seconds
    
    Returns:
        bool if certificate is valid, None if error occurs
    """
    try:
        # Parse URL and validate format
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            logging.error("Invalid URL format")
            return None
            
        # Create secure SSL context
        context = ssl.create_default_context(cafile=certifi.where())
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        
        # Create socket and wrap with SSL
        with socket.create_connection((parsed_url.hostname, 443), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=parsed_url.hostname) as secure_sock:
                # Verify certificate validity
                secure_sock.do_handshake()
                return secure_sock.getpeercert() is not None
                
    except (ssl.SSLCertVerificationError, 
            ssl.SSLError, 
            socket.timeout, 
            socket.gaierror, 
            ValueError) as e:
        logging.error(f"SSL certificate validation failed: {str(e)}")
        return None
```