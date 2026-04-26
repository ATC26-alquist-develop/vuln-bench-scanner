import socket
import threading
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureSocketServer:
    def __init__(self, host: str = '', port: int = 8888):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

    def start(self):
        try:
            # Create a TCP/IP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Set SO_REUSEADDR to allow socket reuse
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind the socket to a specific address and port
            self.socket.bind((self.host, self.port))
            
            # Listen for incoming connections
            self.socket.listen(5)
            
            self.running = True
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    # Wait for a connection
                    client_socket, client_address = self.socket.accept()
                    logging.info(f"New connection from {client_address}")
                    
                    # Handle the client connection in a separate thread
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                    client_thread.start()
                except socket.error as e:
                    logging.error(f"Socket error: {e}")
        except Exception as e:
            logging.error(f"Error starting server: {e}")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()
        logging.info("Server stopped")

    def handle_client(self, client_socket: socket.socket, client_address: Tuple[str, int]):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                # Process received data (implement your logic here)
                response = "Server received: " + data.decode('utf-8')
                client_socket.send(response.encode('utf-8'))
        except socket.error as e:
            logging.error(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {client_address}")

if __name__ == "__main__":
    server = SecureSocketServer()
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("Server shutdown requested")
        server.stop()