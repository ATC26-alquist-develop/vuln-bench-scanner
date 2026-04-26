import socket
import ssl
import logging
from typing import Tuple
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocketConnection:
    def __init__(self, host: str, port: int, ca_cert_path: str):
        """
        Initialize secure socket connection with proper security measures
        
        Args:
            host: Target hostname
            port: Target port
            ca_cert_path: Path to CA certificate file
        """
        self.host = host
        self.port = port
        self.ca_cert_path = ca_cert_path
        self._socket = None
        
    @contextmanager
    def connect(self):
        """Secure context manager for socket connection"""
        try:
            # Create secure SSL context
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, 
                                                cafile=self.ca_cert_path)
            
            # Create socket
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            secure_socket = context.wrap_socket(
                self._socket,
                server_hostname=self.host
            )
            
            # Connect
            secure_socket.connect((self.host, self.port))
            
            logger.info(f"Successfully connected to {self.host}:{self.port}")
            yield secure_socket
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Connection failed: {str(e)}")
            raise
        finally:
            if self._socket:
                try:
                    self._socket.close()
                except Exception as e:
                    logger.error(f"Error closing socket: {str(e)}")