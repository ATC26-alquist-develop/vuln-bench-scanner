```python
import socket
import ssl
import secrets
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureServer:
    def __init__(self, host: str, port: int, cert_file: str, key_file: str):
        """Initialize secure server with TLS"""
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.key_file = key_file
        self.context = self._create_ssl_context()
        
    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        return context

    def start(self) -> None:
        """Start secure server"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)
                logger.info(f"Server listening on {self.host}:{self.port}")
                
                while True:
                    client_socket, addr = server_socket.accept()
                    secure_client = self.context.wrap_socket(client_socket, server_side=True)
                    self._handle_client(secure_client, addr)
                    
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise

    def _handle_client(self, secure_client: ssl.SSLSocket, addr: Tuple[str, int]) -> None:
        """Handle client connection securely"""
        try:
            logger.info(f"New connection from {addr}")
            while True:
                data = secure_client.recv(1024)
                if not data:
                    break
                response = self._process_request(data)
                secure_client.sendall(response)
        except ssl.SSLError as e:
            logger.error(f"SSL error with client {addr}: {e}")
        except Exception as e:
            logger.error(f"Error handling client {addr}: {e}")
        finally:
            secure_client.close()
            logger.info(f"Connection closed for {addr}")

    def _process_request(self, data: bytes) -> bytes:
        """Process client request"""
        # Implement request processing logic here
        return b"Request processed"

class SecureClient:
    def __init__(self, host: str, port: int, cert_file: str):
        """Initialize secure client with TLS"""
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.context = self._create_ssl_context()
        
    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(self.cert_file)
        context.check_hostname = True
        return context

    def connect(self) -> ssl.SSLSocket:
        """Establish secure connection"""
        try:
            with socket.create_connection((self.host, self.port)) as sock:
                secure_sock = self.context.wrap_socket(sock, server_hostname=self.host)
                logger.info(f"Connected to {self.host}:{self.port}")
                return secure_sock
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise

    def send_receive(self, data: bytes) -> bytes:
        """Send data and receive response"""
        try:
            with self.connect() as secure_sock:
                secure_sock.sendall(data)
                return secure_sock.recv(1024)
        except Exception as e:
            logger.error(f"Send/