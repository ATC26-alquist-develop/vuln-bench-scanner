import socket
import ssl
import logging
from typing import Tuple
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_connection(host: str, port: int, timeout: int = 10) -> Tuple[ssl.SSLSocket, ssl.SSLContext]:
    """
    Creates a secure SSL connection to a remote server.
    
    Args:
        host: Server hostname
        port: Server port
        timeout: Connection timeout in seconds
    
    Returns:
        Tuple containing SSL socket and SSL context
    
    Raises:
        ValueError: If invalid parameters provided
        ssl.SSLError: If SSL/TLS handshake fails
    """
    # Validate inputs
    if not isinstance(host, str) or not isinstance(port, int) or not isinstance(timeout, int):
        raise ValueError("Invalid input types")
    
    if port < 1 or port > 65535:
        raise ValueError("Invalid port number")
    
    if timeout <= 0:
        raise ValueError("Timeout must be positive")

    # Create SSL context with secure defaults
    context = ssl.create_default_context()
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set timeout
        sock.settimeout(timeout)
        
        # Wrap socket with SSL
        secure_sock = context.wrap_socket(
            sock,
            server_hostname=urlparse(host).hostname
        )
        
        # Connect
        secure_sock.connect((host, port))
        
        logger.info(f"Successfully connected to {host}:{port}")
        return secure_sock, context
        
    except socket.gaierror as e:
        logger.error(f"DNS lookup failed: {e}")
        raise
    except socket.timeout:
        logger.error("Connection timed out")
        raise
    except ssl.SSLError as e:
        logger.error(f"SSL error: {e}")
        raise
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        raise

def main():
    try:
        # Example usage
        host = "example.com"
        port = 443
        
        # Create connection
        secure_sock, context = create_secure_connection(host, port)
        
        # Perform operations here
        # ...
        
        # Close connection
        secure_sock.close()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()