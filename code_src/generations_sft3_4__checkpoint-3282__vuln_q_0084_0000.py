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

    def create_connection(self) -> None:
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
            logger.info(f"Connected to {self.host}:{self.port}")
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Failed to create socket connection: {str(e)}")
            raise

    def close_connection(self) -> None:
        """Close the socket connection properly."""
        try:
            if self.socket:
                self.socket.close()
                logger.info("Socket connection closed")
                self.socket = None
        except Exception as e:
            logger.error(f"Error closing socket: {str(e)}")
            raise

def main():
    try:
        # Create a secure socket
        secure_socket = SecureSocket("example.com", 443)
        
        # Create connection
        secure_socket.create_connection()
        
        # Perform operations here...
        
        # Close connection
        secure_socket.close_connection()
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()