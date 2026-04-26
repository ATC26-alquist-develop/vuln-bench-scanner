import socket
import ssl
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocket:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket: Optional[ssl.SSLSocket] = None

    def create_secure_connection(self) -> None:
        """Create a secure SSL socket connection."""
        try:
            # Create a secure SSL context
            context = ssl.create_default_context()
            
            # Create a regular socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap the socket with SSL
            self.socket = context.wrap_socket(sock, server_hostname=self.host)
            
            # Establish connection
            self.socket.connect((self.host, self.port))
            logger.info("Secure connection established")
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Failed to create secure connection: {e}")
            self.close_connection()
            raise

    def close_connection(self) -> None:
        """Safely close the socket connection."""
        if self.socket:
            try:
                self.socket.close()
                logger.info("Connection closed successfully")
            except (socket.error, ssl.SSLError) as e:
                logger.error(f"Failed to close connection: {e}")
            finally:
                self.socket = None

# Usage example
if __name__ == "__main__":
    secure_socket = SecureSocket("example.com", 443)
    secure_socket.create_secure_connection()
    # Use the socket...
    secure_socket.close_connection()