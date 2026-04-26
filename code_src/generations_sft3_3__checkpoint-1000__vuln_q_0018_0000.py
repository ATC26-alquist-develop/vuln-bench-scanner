import socket
import ssl
import logging
from typing import Tuple
from urllib.parse import urlparse
import ipaddress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_hostname(hostname: str) -> bool:
    """Validate hostname format."""
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False

def create_secure_connection(
    hostname: str,
    port: int = 443,
    timeout: int = 10
) -> Tuple[ssl.SSLSocket, ssl.SSLContext]:
    """
    Create a secure SSL connection to a remote server.
    
    Args:
        hostname: Target hostname
        port: Target port (default 443 for HTTPS)
        timeout: Connection timeout in seconds
    
    Returns:
        Tuple of (SSL socket, SSL context)
    """
    # Validate hostname
    if not validate_hostname(hostname):
        raise ValueError("Invalid hostname format")
    
    # Create secure SSL context
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_default_certs()

    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set timeout
        sock.settimeout(timeout)
        
        # Create SSL wrapper
        ssl_sock = context.wrap_socket(
            sock,
            server_hostname=hostname
        )
        
        # Connect
        ssl_sock.connect((hostname, port))
        
        return ssl_sock, context
        
    except (socket.timeout, ssl.SSLError, socket.error) as e:
        logger.error(f"Connection failed: {str(e)}")
        raise

def main():
    try:
        # Example usage
        hostname = "example.com"
        ssl_sock, context = create_secure_connection(hostname)
        
        # Perform operations here
        logger.info("Connected successfully")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    main()