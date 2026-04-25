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
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None
        self.context = None

    def start(self):
        try:
            # Create SSL context with secure settings
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")
            self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
            
            # Create and bind socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            logger.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, addr = self.socket.accept()
                logger.info(f"New connection from {addr}")
                
                # Wrap socket with SSL
                secure_client = self.context.wrap_socket(client_socket, server_side=True)
                
                # Handle client in separate thread
                client_thread = threading.Thread(target=self.handle_client, args=(secure_client, addr))
                client_thread.start()
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, addr: Tuple[str, int]):
        try:
            # Generate secure random token
            token = secrets.token_hex(32)
            
            # Send token to client
            client_socket.send(token.encode('utf-8'))
            
            # Receive response from client
            response = client_socket.recv(1024).decode('utf-8')
            
            # Verify response (implement your own logic)
            if not self.verify_response(response):
                raise ValueError("Invalid response")
            
            logger.info(f"Received valid response from {addr}")
        except Exception as e:
            logger.error(f"Error handling client {addr}: {str(e)}")
        finally:
            client_socket.close()

    def verify_response(self, response: str) -> bool:
        # Implement your own response verification logic
        return True

class SecureClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = None

    def connect(self):
        try:
            # Create SSL context with secure settings
            self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.context.check_hostname = True
            self.context.verify_mode = ssl.CERT_REQUIRED
            
            # Connect to server
            self.socket = socket.create_connection((self.host, self.port))
            self.secure_socket = self.context.wrap_socket(self.socket, server_hostname=self.host)
            
            logger.info(f"Connected to {self.host}:{self.port}")
            
            # Receive token
            token = self.secure_socket.recv(1024).decode('utf-8')
            
            # Send response (implement your own logic)
            response = "Valid"
            self.secure_socket.send(response.encode('utf-8'))
            
            logger.info("Response sent successfully")
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()

# Usage example
if __name__ == "__main__":
    # Server
    server = SecureServer('localhost', 8443)
    server_thread =