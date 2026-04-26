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
        """Initialize secure server with proper SSL/TLS configuration."""
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.key_file = key_file
        self.socket = None
        self.context = None
        
    def setup_ssl_context(self) -> None:
        """Set up secure SSL context with strong security settings."""
        try:
            # Create SSL context with secure defaults
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
            
            # Enforce strong cipher suites
            self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
            
            # Force TLS 1.2 or higher
            self.context.minimum_version = ssl.TLSVersion.TLSv1_2
            
        except ssl.SSLError as e:
            logger.error(f"SSL context setup failed: {e}")
            raise
            
    def start_server(self) -> None:
        """Start the secure server."""
        try:
            # Create TCP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket to address
            self.socket.bind((self.host, self.port))
            
            # Start listening for connections
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
                client_handler = threading.Thread(
                    target=self.handle_client,
                    args=(secure_client, address)
                )
                client_handler.start()
                
        except Exception as e:
            logger.error(f"Server error: {e}")
            if self.socket:
                self.socket.close()
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle individual client connections securely."""
        try:
            logger.info(f"New connection from {address}")
            
            # Generate secure session token
            session_token = secrets.token_hex(32)
            
            # Handle client communication
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                    
                # Process received data (implement your logic here)
                response = f"Server received: {data.decode('utf-8')}"
                client_socket.send(response.encode('utf-8'))
                
        except ssl.SSLError as e:
            logger.error(f"SSL error with client {address}: {e}")
        except Exception as e:
            logger.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"Connection closed for {address}")

def main():
    # Example usage
    host = 'localhost'
    port = 8443
    cert_file = 'path/to/cert.pem'
    key_file = 'path/to/key.pem'
    
    try:
        ssl_context = SecureServer(host, port, cert_file, key_file)
        ssl_context.setup_ssl_context()
        ssl_context.start_server()
        
    except Exception