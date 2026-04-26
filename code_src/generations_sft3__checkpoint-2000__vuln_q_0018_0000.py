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
        self.host = host
        self.port = port
        self.ca_cert_path = ca_cert_path
        self.socket = None
        self.context = None
        
    @contextmanager
    def secure_connection(self):
        """Secure context manager for socket connections."""
        try:
            # Create SSL context with secure defaults
            self.context = ssl.create_default_context(cafile=self.ca_cert_path)
            
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            secure_socket = self.context.wrap_socket(
                self.socket,
                server_hostname=self.host
            )
            
            yield secure_socket
            
        except ssl.SSLError as e:
            logger.error(f"SSL error occurred: {e}")
            raise
        except socket.error as e:
            logger.error(f"Socket error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            raise
        finally:
            if self.socket:
                try:
                    self.socket.close()
                except Exception:
                    pass
                self.socket = None
            if self.context:
                try:
                    self.context.close()
                except Exception:
                    pass
                self.context = None

    def connect(self) -> Tuple[bool, str]:
        """Establish secure connection to remote server."""
        try:
            # Validate inputs
            if not isinstance(self.host, str) or not isinstance(self.port, int):
                raise ValueError("Invalid host or port format")
            
            if self.port < 1 or self.port > 65535:
                raise ValueError("Port must be between 1 and 65535")
            
            # Connect to server
            self.socket = self.context.wrap_socket(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                server_hostname=self.host
            )
            self.socket.connect((self.host, self.port))
            
            logger.info(f"Successfully connected to {self.host}:{self.port}")
            return True, "Connection successful"
            
        except ssl.SSLError as e:
            logger.error(f"SSL error occurred: {e}")
            return False, str(e)
        except socket.error as e:
            logger.error(f"Socket error occurred: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return False, str(e)

    def close(self):
        """Safely close the connection."""
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
            self.socket = None