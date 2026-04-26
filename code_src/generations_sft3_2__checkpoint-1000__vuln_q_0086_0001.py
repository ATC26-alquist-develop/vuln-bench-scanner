import socket
import threading
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EchoServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8888):
        self.host = host
        self.port = port
        self.sock = None

    def start(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client, address = self.sock.accept()
                client_handler = threading.Thread(target=self.handle_client, args=(client, address))
                client_handler.start()
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
        finally:
            if self.sock:
                self.sock.close()

    def handle_client(self, client_socket: socket.socket, address: Tuple[str, int]):
        try:
            logging.info(f"New connection from {address}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                client_socket.sendall(data)
        except Exception as e:
            logging.error(f"Error handling client {address}: {str(e)}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

if __name__ == "__main__":
    server = EchoServer()
    server.start()