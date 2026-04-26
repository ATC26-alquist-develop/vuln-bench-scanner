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
        self.context = None
        
    @contextmanager
    def create_secure_connection(self):
        """Create a secure SSL/TLS connection with proper error handling"""
        try:
            # Create SSL context with secure defaults
            self.context = ssl.create_default_context()
            self.context.check_hostname = True
            self.context.verify_mode = ssl.CERT_REQUIRED
            
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            secure_socket = self.context.wrap_socket(
                self.socket,
                server_hostname=self.host
            )
            
            logger.info(f"Established secure connection to {self.host}:{self.port}")
            yield secure_socket
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Connection error: {str(e)}")
            raise
            
        finally:
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
                
    def __del__(self):
        """Ensure proper cleanup"""
        if self.context:
            self.context = None

def connect_to_server(host: str, port: int) -> Tuple[bool, str]:
    """
    Connect to server securely and return connection status and message
    """
    try:
        secure_socket = SecureSocket(host, port)
        
        with secure_socket.create_secure_connection() as conn:
            conn.connect((host, port))
            return True, "Connection successful"
            
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        return False, str(e)

# Example usage
if __name__ == "__main__":
    success, message = connect_to_server("example.com", 443)
    if success:
        print(f"Success: {message}")
    else:
        print(f"Error: {message}")