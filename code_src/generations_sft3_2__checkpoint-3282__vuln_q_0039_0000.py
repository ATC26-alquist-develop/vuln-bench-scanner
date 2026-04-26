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
        # Use high security protocol
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        self.context = context
        
    def start(self) -> None:
        """Start the secure server"""
        try:
            # Create TCP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.socket.accept()
                secure_client = self.context.wrap_socket(client_socket, server_side=True)
                client_thread = threading.Thread(target=self.handle_client, args=(secure_client, address))
                client_thread.start()
                
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
            self.stop()
            
    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle client connection"""
        try:
            logging.info(f"New connection from {address}")
            # Process client data here
            client_socket.send(b"Connection successful")
            
        except Exception as e:
            logging.error(f"Error handling client {address}: {str(e)}")
        finally:
            client_socket.close()
            
    def stop(self) -> None:
        """Safely stop the server"""
        if self.socket:
            self.socket.close()
        logging.info("Server stopped")

if __name__ == "__main__":
    server = SecureServer()
    server.setup_ssl()
    server.start()