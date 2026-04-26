import socket
import ssl
import threading
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecureServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8443):
        self.host = host
        self.port = port
        self.socket = None
        self.context = None
        
    def setup_ssl(self) -> None:
        """Set up secure SSL context"""
        # Use strong TLS configuration
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        self.context.options |= ssl.OP_NO_COMPRESSION  # Prevent downgrade attacks
        self.context.verify_mode = ssl.CERT_REQUIRED  # Verify client certificates
        self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    def start(self) -> None:
        """Start the secure server"""
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.socket.accept()
                # Wrap socket with SSL
                secure_client = self.context.wrap_socket(client_socket, server_side=True)
                client_handler = threading.Thread(
                    target=self.handle_client,
                    args=(secure_client, address)
                )
                client_handler.start()
                
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
            self.socket.close()
            
    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle individual client connections"""
        try:
            logging.info(f"New connection from {address}")
            # Implement proper authentication and authorization here
            client_socket.send(b"Welcome to the secure server!")
            
        except Exception as e:
            logging.error(f"Error handling client {address}: {str(e)}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = SecureServer()
    server.setup_ssl()
    server.start()