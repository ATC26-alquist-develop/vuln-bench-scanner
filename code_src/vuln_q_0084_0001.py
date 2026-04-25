```python
import socket
import ssl
import secrets
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None
        self.context = None

    def start(self):
        try:
            # Create SSL context with secure settings
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
            self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
            
            # Create and bind socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            logger.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, addr = self.socket.accept()
                self.handle_client(client_socket, addr)
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, addr: Tuple[str, int]):
        try:
            # Wrap socket with SSL
            secure_socket = self.context.wrap_socket(client_socket, server_side=True)
            
            # Generate secure random token
            token = secrets.token_hex(32)
            
            # Send token to client
            secure_socket.sendall(token.encode('utf-8'))
            
            # Receive message from client
            data = secure_socket.recv(1024).decode('utf-8')
            
            # Process data (example: echo back)
            response = f"Server received: {data}"
            secure_socket.sendall(response.encode('utf-8'))
            
            logger.info(f"Connection from {addr}: {data}")
        except ssl.SSLError as e:
            logger.error(f"SSL error: {str(e)}")
        except Exception as e:
            logger.error(f"Error handling client {addr}: {str(e)}")
        finally:
            secure_socket.close()

class SecureSocketClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = None

    def connect(self):
        try:
            # Create SSL context
            self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.context.check_hostname = True
            self.context.verify_mode = ssl.CERT_REQUIRED
            
            # Connect to server
            with socket.create_connection((self.host, self.port)) as sock:
                with self.context.wrap_socket(sock, server_hostname=self.host) as secure_sock:
                    logger.info(f"Connected to {self.host}:{self.port}")
                    
                    # Receive token
                    token = secure_sock.recv(1024).decode('utf-8')
                    logger.info(f"Received token: {token}")
                    
                    # Send message
                    message = "Hello, server!"
                    secure_sock.sendall(message.encode('utf-8'))
                    
                    # Receive response
                    response = secure_sock.recv(1024).decode('utf-8')
                    logger.info(f"Received response: {response}")
        except ssl.SSLError as e:
            logger.error(f"SSL error: {str(e)}")
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")

# Usage example
if __name__ == "__main__":