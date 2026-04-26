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
        host: Server hostname or IP
        port: Server port (typically 443 for HTTPS)
        timeout: Connection timeout in seconds
    
    Returns:
        Tuple of (SSL socket, SSL context)
    """
    try:
        # Validate inputs
        if not isinstance(host, str) or not isinstance(port, int) or not isinstance(timeout, int):
            raise ValueError("Invalid input types")
        
        if port < 1 or port > 65535:
            raise ValueError("Invalid port number")
        
        if timeout <= 0:
            raise ValueError("Timeout must be positive")

        # Create SSL context with secure defaults
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        
        # Create secure socket
        sock = socket.create_connection((host, port), timeout=timeout)
        
        # Wrap socket with SSL
        secure_sock = context.wrap_socket(sock, server_hostname=urlparse(host).hostname)
        
        logger.info(f"Successfully connected to {host}:{port}")
        return secure_sock, context

    except (socket.error, ssl.SSLError, ValueError) as e:
        logger.error(f"Connection failed: {str(e)}")
        raise

def close_connection(ssl_socket: ssl.SSLSocket) -> None:
    """Safely closes the SSL connection"""
    try:
        ssl_socket.shutdown(socket.SHUT_RDWR)
        ssl_socket.close()
        logger.info("Connection closed successfully")
    except Exception as e:
        logger.error(f"Error closing connection: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        # Create connection
        conn, context = create_secure_connection("example.com", 443)
        
        # Use connection...
        # ...
        
        # Close connection
        close_connection(conn)
    except Exception as e:
        logger.error(f"Error: {str(e)}")