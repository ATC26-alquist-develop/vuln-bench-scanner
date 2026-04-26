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
        """Initialize secure socket connection with proper security measures."""
        if not isinstance(host, str) or not host:
            raise ValueError("Invalid host")
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError("Invalid port")
        if not isinstance(ca_cert_path, str) or not ca_cert_path:
            raise ValueError("Invalid CA certificate path")
            
        self.host = host
        self.port = port
        self.ca_cert_path = ca_cert_path
        self.socket = None
        self.context = None

    @contextmanager
    def connect(self):
        """Securely establish and manage socket connection."""
        try:
            # Create SSL context with secure defaults
            self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.context.load_verify_locations(cafile=self.ca_cert_path)
            
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            secure_socket = self.context.wrap_socket(
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
                except Exception as e:
                    logger.error(f"Error closing socket: {str(e)}")