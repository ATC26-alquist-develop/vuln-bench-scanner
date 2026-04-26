import socket
import threading
import logging
from typing import Tuple
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8443):
        self.host = host
        self.port = port
        self.socket = None
        self.context = None
        
    def start(self):
        """Start the secure server"""
        try:
            # Create SSL context
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")
            
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            logger.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.socket.accept()
                secure_client = self.context.wrap_socket(client_socket, server_side=True)
                client_thread = threading.Thread(target=self.handle_client, args=(secure_client, address))
                client_thread.start()
                
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]):
        """Handle client connections"""
        try:
            logger.info(f"New connection from {address}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process received data here
                response = "Server received: " + data.decode('utf-8')
                client_socket.send(response.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error handling client {address}: {str(e)}")
        finally:
            client_socket.close()
            logger.info(f"Connection closed for {address}")

if __name__ == "__main__":
    server = SecureServer()
    server.start()