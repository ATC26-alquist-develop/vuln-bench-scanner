import socket
import ssl
import logging
from typing import Tuple
from urllib.parse import urlparse
import ipaddress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocketConnection:
    def __init__(self, host: str, port: int, timeout: float = 10.0):
        """
        Initialize secure socket connection with proper validation
        
        Args:
            host: Server hostname or IP address
            port: Port number
            timeout: Connection timeout in seconds
        """
        # Validate port number
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError("Invalid port number")
        
        # Validate and parse hostname/IP
        try:
            self.host = str(ipaddress.ip_address(host))
        except ValueError:
            self.host = host
            
        self.port = port
        self.timeout = timeout
        self.context = None
        
    def create_secure_connection(self) -> Tuple[ssl.SSLSocket, ssl.SSLContext]:
        """
        Create a secure SSL connection to the remote server
        
        Returns:
            Tuple containing SSL socket and SSL context
        """
        try:
            # Create SSL context with secure defaults
            self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.context.check_hostname = True
            self.context.verify_mode = ssl.CERT_REQUIRED
            
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Set timeout
            sock.settimeout(self.timeout)
            
            # Wrap socket with SSL
            secure_sock = self.context.wrap_socket(
                sock,
                server_hostname=self.host
            )
            
            # Verify certificate
            secure_sock.verify_certificate()
            
            logger.info("Secure connection established")
            return secure_sock, self.context
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Connection error: {str(e)}")
            raise
            
    def close(self):
        """
        Safely close the connection
        """
        if self.context:
            self.context.close()
        if hasattr(self, 'secure_sock'):
            self.secure_sock.close()

def main():
    try:
        # Example usage
        host = "example.com"
        port = 443
        
        connection = SecureSocketConnection(host, port)
        secure_sock, context = connection.create_secure_connection()
        
        # Perform operations here
        secure_sock.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
        
        # Read response
        response = secure_sock.recv(4096)
        
        # Process response
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()