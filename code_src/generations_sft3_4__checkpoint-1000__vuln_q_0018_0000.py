import socket
import ssl
import logging
from typing import Tuple
from urllib.parse import urlparse
import ipaddress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_connection(host: str, port: int, timeout: float = 5.0) -> Tuple[ssl.SSLSocket, ssl.SSLContext]:
    """
    Create a secure SSL connection to a remote server.
    
    Args:
        host: Server hostname or IP address
        port: Server port number
        timeout: Connection timeout in seconds
    
    Returns:
        Tuple containing SSL socket and SSL context
    
    Raises:
        ValueError: If host or port is invalid
        ssl.SSLError: If SSL/TLS handshake fails
    """
    try:
        # Validate host and port
        parsed = urlparse(host)
        if not parsed.hostname or not parsed.port:
            raise ValueError("Invalid host format")
        
        # Validate IP address
        ipaddress.ip_address(parsed.hostname)
        
        # Create secure SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set timeout
        sock.settimeout(timeout)
        
        # Create SSL socket
        ssl_sock = context.wrap_socket(sock, server_hostname=parsed.hostname)
        
        # Connect
        ssl_sock.connect((parsed.hostname, parsed.port))
        
        return ssl_sock, context
        
    except (socket.error, ssl.SSLError, ValueError) as e:
        logger.error(f"Connection failed: {str(e)}")
        raise

def main():
    try:
        # Example usage
        host = "example.com"
        port = 443
        
        # Create secure connection
        ssl_sock, context = create_secure_connection(host, port)
        
        # Perform operations here
        ssl_sock.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
        
        # Receive response
        response = ssl_sock.recv(4096)
        
        print(f"Received response: {response.decode('utf-8', errors='replace')}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        if 'ssl_sock' in locals():
            ssl_sock.close()

if __name__ == "__main__":
    main()