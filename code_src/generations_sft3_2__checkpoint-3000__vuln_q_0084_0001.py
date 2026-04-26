import socket
import ssl
import secrets
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocket:
    def __init__(self, host: str, port: int, cert_path: str, key_path: str):
        """Initialize secure socket with TLS"""
        self.host = host
        self.port = port
        self.cert_path = cert_path
        self.key_path = key_path
        self.sock: Optional[ssl.SSLSocket] = None
        
    def start_server(self) -> None:
        """Start secure server"""
        try:
            # Create SSL context with secure defaults
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=self.cert_path, keyfile=self.key_path)
            
            # Create socket and wrap with SSL
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock = context.wrap_socket(self.sock, server_side=True)
            
            # Bind socket to address
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            
            logger.info(f"Secure server started on {self.host}:{self.port}")
            
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            self.close()
            raise
            
    def accept_connection(self) -> Tuple[ssl.SSLSocket, Tuple[str, int]]:
        """Accept client connection"""
        try:
            client_sock, address = self.sock.accept()
            return client_sock, address
        except ssl.SSLError as e:
            logger.error(f"SSL error during connection: {e}")
            self.close()
            raise
        except Exception as e:
            logger.error(f"Error accepting connection: {e}")
            self.close()
            raise
            
    def send_data(self, data: bytes) -> None:
        """Send data securely"""
        if not self.sock:
            raise RuntimeError("Socket not initialized")
        try:
            self.sock.sendall(data)
        except ssl.SSLError as e:
            logger.error(f"SSL error during send: {e}")
            self.close()
            raise
        except Exception as e:
            logger.error(f"Error sending data: {e}")
            self.close()
            raise
            
    def receive_data(self, max_size: int = 4096) -> bytes:
        """Receive data securely"""
        if not self.sock:
            raise RuntimeError("Socket not initialized")
        try:
            return self.sock.recv(max_size)
        except ssl.SSLError as e:
            logger.error(f"SSL error during receive: {e}")
            self.close()
            raise
        except Exception as e:
            logger.error(f"Error receiving data: {e}")
            self.close()
            raise
            
    def close(self) -> None:
        """Safely close the socket"""
        if self.sock:
            try:
                self.sock.close()
            except Exception as e:
                logger.error(f"Error closing socket: {e}")
            finally:
                self.sock = None