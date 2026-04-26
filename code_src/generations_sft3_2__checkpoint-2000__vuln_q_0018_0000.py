import socket
import ssl
import logging
from typing import Tuple
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocket:
    def __init__(self, host: str, port: int, ca_cert_path: str):
        """Initialize secure socket with proper certificate validation."""
        self.host = host
        self.port = port
        self.ca_cert_path = ca_cert_path
        self.socket = None
        
    @contextmanager
    def create_secure_connection(self):
        """Create and manage secure socket connection."""
        try:
            # Create SSL context with secure defaults
            context = ssl.create_default_context(cafile=self.ca_cert_path)
            
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            secure_socket = context.wrap_socket(
                self.socket,
                server_hostname=self.host
            )
            
            # Connect to server
            secure_socket.connect((self.host, self.port))
            
            logger.info(f"Secure connection established to {self.host}:{self.port}")
            yield secure_socket
            
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

def main():
    # Example usage
    try:
        # Initialize secure socket
        secure_conn = SecureSocket("example.com", 443, "/path/to/ca_cert.pem")
        
        # Create secure connection
        with secure_conn.create_secure_connection() as conn:
            # Perform secure operations here
            pass
            
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}")

if __name__ == "__main__":
    main()