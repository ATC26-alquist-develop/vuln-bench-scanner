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

    def start_server(self) -> None:
        """Start secure server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            # Set secure socket options
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setblocking(0)
            
            self.setup_ssl_context()
            
            logger.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                try:
                    client_socket = self.accept_connection()
                    if client_socket:
                        client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                        client_thread.start()
                except Exception as e:
                    logger.error(f"Error in server loop: {e}")
                    
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            self.cleanup()
            
    def accept_connection(self) -> ssl.SSLSocket:
        """Securely accept client connection"""
        try:
            client_socket, address = self.socket.accept()
            secure_socket = self.context.wrap_socket(client_socket, server_side=True)
            logger.info(f"Accepted connection from {address}")
            return secure_socket
        except ssl.SSLError as e:
            logger.error(f"SSL error during connection: {e}")
            raise
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return None

    def handle_client(self, client_socket: ssl.SSLSocket) -> None:
        """Handle client connection securely"""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process data here
                response = "Received: " + data.decode('utf-8')
                client_socket.send(response.encode('utf-8'))
        except ssl.SSLError as e:
            logger.error(f"SSL error in client handler: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in client handler: {e}")
        finally:
            client_socket.close()
            logger.info("Client connection closed")

    def cleanup(self) -> None:
        """Clean up resources"""
        try:
            if self.socket:
                self.socket.close()
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")
        finally:
            self.socket = None
            self.context = None

class SecureClient:
    def __init__(self, host: str, port: int, cert_file: str):
        """Initialize secure client"""
        self.host = host
        self.port = port
        self.cert_file = cert_file