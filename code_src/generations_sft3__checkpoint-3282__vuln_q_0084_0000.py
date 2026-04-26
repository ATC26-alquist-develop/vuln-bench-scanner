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
        self.socket: Optional[socket.socket] = None

    def create_connection(self) -> None:
        """Create a secure socket connection."""
        try:
            # Create a secure SSL context
            context = ssl.create_default_context()
            
            # Create a socket object
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap the socket with SSL
            secure_socket = context.wrap_socket(
                self.socket,
                server_hostname=self.host
            )
            
            # Connect to the server
            secure_socket.connect((self.host, self.port))
            
            logger.info(f"Secure connection established to {self.host}:{self.port}")
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Failed to create secure connection: {str(e)}")
            self.close_connection()
            raise

    def close_connection(self) -> None:
        """Safely close the socket connection."""
        if self.socket:
            try:
                self.socket.close()
                logger.info("Socket connection closed")
            except socket.error as e:
                logger.error(f"Error closing socket: {str(e)}")
            finally:
                self.socket = None

def main():
    try:
        # Create an instance of SecureSocket
        secure_socket = SecureSocket("example.com", 443)
        
        # Create and close the connection
        secure_socket.create_connection()
        secure_socket.close_connection()
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()