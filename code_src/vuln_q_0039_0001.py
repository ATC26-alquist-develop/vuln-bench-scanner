import socket
import threading
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)

class SecureServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 8888):
        self.host = host
        self.port = port
        self.socket = None

    def start(self):
        """Start the server and listen for incoming connections."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, client_address = self.socket.accept()
                logging.info(f"New connection from {client_address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: socket.socket, client_address: Tuple[str, int]):
        """Handle communication with a connected client."""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                response = self.process_data(data)
                client_socket.sendall(response)
        except Exception as e:
            logging.error(f"Error handling client {client_address}: {str(e)}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {client_address}")

    def process_data(self, data: bytes) -> bytes:
        """Process received data and return a response."""
        try:
            # Simple echo server implementation
            return data
        except Exception as e:
            logging.error(f"Error processing data: {str(e)}")
            return b"Error processing data"

if __name__ == "__main__":
    server = SecureServer()
    server.start()