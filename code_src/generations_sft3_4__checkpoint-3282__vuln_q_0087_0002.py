```python
import socket
import ssl
import threading
import logging
from typing import Tuple
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            # Create SSL context with secure defaults
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
            self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
            self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        except Exception as e:
            logging.error(f"SSL context setup failed: {e}")
            raise

    def start_server(self) -> None:
        """Start secure server"""
        try:
            # Create TCP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket to address
            self.socket.bind((self.host, self.port))
            
            # Start listening for connections
            self.socket.listen(5)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.socket.accept()
                secure_client = ssl_context.wrap_socket(
                    client_socket,
                    server_side=True,
                    certfile=self.cert_file,
                    keyfile=self.key_file,
                    ssl_version=ssl.PROTOCOL_TLS_CLIENT
                )
                client_handler = threading.Thread(target=self.handle_client, args=(secure_client, address))
                client_handler.start()
                
        except Exception as e:
            logging.error(f"Server error: {e}")
            self.socket.close()
            raise

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle client connection securely"""
        try:
            logging.info(f"New connection from {address}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process data (implement your logic here)
                response = "Received: " + data.decode('utf-8')
                client_socket.send(response.encode('utf-8'))
        except ssl.SSLError as e:
            logging.error(f"SSL error with client {address}: {e}")
        except Exception as e:
            logging.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

def main():
    # Example usage
    try:
        # Set up secure SSL context
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')
        ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        
        # Create and start server
        server = SecureServer('localhost', 8443, 'server.crt', 'server.key')
        server.setup_ssl_context()
        server.start_server()
        
    except Exception as e:
        logging.error(f"Server initialization failed: {e}")

if __name__ == "__