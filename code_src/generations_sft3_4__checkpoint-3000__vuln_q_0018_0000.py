import socket
import ssl
import logging
from typing import Tuple
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocket:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None
        self.context = ssl.create_default_context()
        
    @contextmanager
    def connect(self):
        """Securely establish and manage socket connection"""
        try:
            # Create secure socket
            self.socket = self.context.wrap_socket(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                server_hostname=self.host
            )
            
            # Set timeout to prevent hanging
            self.socket.settimeout(30)
            
            # Connect to server
            self.socket.connect((self.host, self.port))
            logger.info(f"Successfully connected to {self.host}:{self.port}")
            yield self.socket
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Connection error: {str(e)}")
            raise
        finally:
            if self.socket:
                try:
                    self.socket.close()
                    logger.info("Connection closed")
                except Exception as e:
                    logger.error(f"Error closing socket: {str(e)}")

def get_server_address() -> Tuple[str, int]:
    """Get server address from environment variables"""
    try:
        host = os.environ.get('SERVER_HOST')
        port = int(os.environ.get('SERVER_PORT', '443'))
        if not host or not isinstance(port, int):
            raise ValueError("Invalid server address configuration")
        return host, port
    except (ValueError, TypeError):
        raise ValueError("Invalid server address configuration")

def main():
    try:
        # Get server address from environment variables
        host, port = get_server_address()
        
        # Create secure socket
        secure_socket = SecureSocket(host, port)
        
        # Establish connection
        with secure_socket.connect() as conn:
            # Perform operations here
            logger.info("Connected successfully")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()