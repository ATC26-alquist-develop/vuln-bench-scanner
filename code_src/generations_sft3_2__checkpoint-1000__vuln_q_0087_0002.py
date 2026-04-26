```python
import socket
import threading
import ssl
import logging
from typing import Tuple
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureServer:
    def __init__(self, host: str, port: int, cert_file: str, key_file: str):
        """Initialize secure server with proper SSL/TLS configuration."""
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.key_file = key_file
        self.socket = None
        self.running = False
        
        # Configure SSL context
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
        
    def start(self):
        """Start the secure server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    secure_client = self.context.wrap_socket(client_socket, server_side=True)
                    client_thread = threading.Thread(target=self.handle_client, args=(secure_client, address))
                    client_thread.start()
                except ssl.SSLError as e:
                    logging.error(f"SSL error: {e}")
                except Exception as e:
                    logging.error(f"Error accepting connection: {e}")
                    
        except Exception as e:
            logging.error(f"Server error: {e}")
        finally:
            self.stop()
            
    def stop(self):
        """Stop the server gracefully."""
        self.running = False
        if self.socket:
            self.socket.close()
        logging.info("Server stopped")

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]):
        """Handle individual client connections."""
        try:
            logging.info(f"New connection from {address}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process received data (implement your logic here)
                response = self.process_data(data)
                client_socket.send(response)
        except ssl.SSLError as e:
            logging.error(f"SSL error with client {address}: {e}")
        except Exception as e:
            logging.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

    def process_data(self, data: bytes) -> bytes:
        """Process received data (implement your logic here)."""
        # Implement your data processing logic
        # This is a placeholder implementation
        return b"Server received: " + data

class SecureClient:
    def __init__(self, host: str, port: int, cert_file: str):
        """Initialize secure client with proper SSL/TLS configuration."""
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.socket = None
        self.running = False
        
        # Configure SSL context
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = True
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.load_verify_locations(cert_file)
        
    def connect(self):
        """Establish secure connection to the server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = self.context.wrap_socket(self.socket, server_hostname=self.host)
            self.socket.connect((self.host, self.port))
            self.running = True