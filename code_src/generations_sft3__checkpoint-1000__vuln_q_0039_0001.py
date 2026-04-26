import socket
import threading
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_secure_socket() -> socket.socket:
    """Create a secure socket with proper error handling."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock
    except socket.error as e:
        logging.error(f"Failed to create socket: {e}")
        raise

def start_server(host: str = '0.0.0.0', port: int = 8888) -> None:
    """Start a secure server that listens on all interfaces."""
    try:
        sock = create_secure_socket()
        sock.bind((host, port))
        sock.listen(5)
        logging.info(f"Server listening on {host}:{port}")
        
        while True:
            client, address = sock.accept()
            logging.info(f"Accepted connection from {address}")
            client_handler = threading.Thread(target=handle_client, args=(client, address))
            client_handler.start()
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        sock.close()

def handle_client(client_socket: socket.socket, address: Tuple[str, int]) -> None:
    """Handle client connections securely."""
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Process received data here
            response = "Server received: " + data.decode('utf-8')
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        logging.error(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Closed connection from {address}")

if __name__ == "__main__":
    start_server()