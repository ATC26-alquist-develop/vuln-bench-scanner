```python
import socket
import ssl
import secrets
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureClientServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.ssl_context = self._create_ssl_context()
        self.client_socket = None
        self.server_socket = None

    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create a secure SSL context with strong security settings"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        context.options |= ssl.OP_NO_COMPRESSION  # Disable compression
        return context

    def start_server(self) -> None:
        """Start a secure server"""
        try:
            # Create socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to address and port
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            logging.info(f"Server listening on {self.host}:{self.port}")
            
            while True:
                client_socket, addr = self.server_socket.accept()
                # Wrap the socket with SSL
                secure_client = self.ssl_context.wrap_socket(client_socket, server_side=True)
                logging.info(f"New connection from {addr}")
                
                # Handle client connection
                self.handle_client(secure_client, addr)
                
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
        finally:
            self.cleanup()

    def handle_client(self, client_socket: ssl.SSLSocket, addr: Tuple[str, int]) -> None:
        """Handle client connection securely"""
        try:
            # Generate a secure random token for session
            session_token = secrets.token_hex(32)
            
            # Send session token to client
            client_socket.sendall(session_token.encode('utf-8'))
            
            # Receive data from client
            data = client_socket.recv(1024)
            if data:
                # Process received data
                response = f"Server received: {data.decode('utf-8')}"
                client_socket.sendall(response.encode('utf-8'))
            
        except ssl.SSLError as e:
            logging.error(f"SSL error with {addr}: {str(e)}")
        except Exception as e:
            logging.error(f"Error handling client {addr}: {str(e)}")
        finally:
            client_socket.close()

    def start_client(self) -> None:
        """Start a secure client"""
        try:
            # Create socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap the socket with SSL
            secure_server = self.ssl_context.wrap_socket(self.client_socket, server_hostname=self.host)
            
            # Connect to server
            secure_server.connect((self.host, self.port))
            logging.info(f"Connected to {self.host}:{self.port}")
            
            # Send session token
            session_token = secrets.token_hex(32)
            secure_server.sendall(session_token.encode('utf-8'))
            
            # Receive and process data
            data = secure_server.recv(1024)
            if data:
                response = data.decode('utf-8')
                logging.info(f"Server response: {response}")
            
        except ssl.SSLError as