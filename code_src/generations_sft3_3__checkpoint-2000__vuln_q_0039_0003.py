import socket
import threading
import logging
from typing import Tuple
import ssl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='server.log'
)

class SecureTCPServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8443):
        self.host = host
        self.port = port
        self.socket = None
        self.context = None
        
        # Create SSL context
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        
    def start(self):
        try:
            # Create TCP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket to address
            self.socket.bind((self.host, self.port))
            
            # Listen for connections
            self.socket.listen(5)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.socket.accept()
                secure_client = self.context.wrap_socket(client_socket, server_side=True)
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(secure_client, address)
                )
                client_thread.start()
                
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]):
        try:
            logging.info(f"New connection from {address}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process received data here
                response = "Message received".encode()
                client_socket.sendall(response)
        except Exception as e:
            logging.error(f"Error handling client {address}: {str(e)}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

if __name__ == "__main__":
    server = SecureTCPServer()
    server.start()