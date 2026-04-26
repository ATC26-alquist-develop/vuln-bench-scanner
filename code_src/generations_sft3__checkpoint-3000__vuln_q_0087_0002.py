```python
import socket
import ssl
import threading
import logging
from typing import Tuple
import secrets

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
        self.socket = None
        self.context = None
        
    def setup_ssl_context(self) -> None:
        """Set up secure SSL context"""
        try:
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
            self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        except ssl.SSLError as e:
            logger.error(f"SSL context setup failed: {e}")
            raise

    def start(self) -> None:
        """Start the secure server"""
        try:
            self.setup_ssl_context()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            logger.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.socket.accept()
                secure_client = ssl_context.wrap_socket(
                    client_socket,
                    server_side=True,
                    certfile=self.cert_file,
                    keyfile=self.key_file
                )
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(secure_client, address)
                )
                client_thread.start()
                
        except ssl.SSLError as e:
            logger.error(f"SSL error: {e}")
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle client connections securely"""
        try:
            logger.info(f"New connection from {address}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process data here
                response = f"Server received: {data.decode('utf-8')}"
                client_socket.send(response.encode('utf-8'))
        except ssl.SSLError as e:
            logger.error(f"SSL error with client {address}: {e}")
        except Exception as e:
            logger.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"Connection closed for {address}")

class SecureClient:
    def __init__(self, host: str, port: int, cert_file: str):
        """Initialize secure client with TLS"""
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.context = None
        
    def setup_ssl_context(self) -> None:
        """Set up secure SSL context"""
        try:
            self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.context.load_verify_locations(self.cert_file)
            self.context.check_hostname = True
            self.context.verify_mode = ssl.CERT_REQUIRED
        except ssl.SSLError as e:
            logger.error(f"SSL context setup failed: {e}")
            raise

    def connect(self) -> ssl.SSLSocket:
        """Establish secure connection"""
        try:
            sock = socket.create_connection((self.host, self.port))
            secure_socket = self.context.wrap_socket(