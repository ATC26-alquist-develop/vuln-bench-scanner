```python
import socket
import ssl
import logging
from typing import List, Tuple
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_connection(host: str, port: int, timeout: float = 10.0) -> Tuple[ssl.SSLSocket, ssl.SSLContext]:
    """
    Create a secure SSL connection to a server.
    
    Args:
        host: Server hostname
        port: Server port
        timeout: Connection timeout in seconds
    
    Returns:
        Tuple of (ssl.SSLSocket, ssl.SSLContext)
    """
    try:
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                logger.info(f"Secure connection established to {host}:{port}")
                return secure_sock, context
    except (socket.timeout, ssl.SSLError, socket.error) as e:
        logger.error(f"Failed to connect to {host}:{port}: {str(e)}")
        raise

def validate_url(url: str) -> bool:
    """Validate URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def main():
    # Example usage with validated URLs
    servers = [
        "example.com:443",
        "secure.example.com:8443"
    ]
    
    for server in servers:
        if not validate_url(server):
            logger.error(f"Invalid URL: {server}")
            continue
            
        host, port = server.split(':')
        try:
            secure_sock, context = create_secure_connection(host, int(port))
            # Use secure_sock for communication
            secure_sock.close()
        except Exception as e:
            logger.error(f"Error processing {server}: {str(e)}")

if __name__ == "__main__":
    main()
```