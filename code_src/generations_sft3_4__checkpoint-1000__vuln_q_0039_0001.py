import socket
import threading
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
    """Handle client connection securely."""
    try:
        logging.info(f"New connection from {client_address}")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Process received data here
            response = "Server received: " + data.decode('utf-8')
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        logging.error(f"Error handling client {client_address}: {str(e)}")
    finally:
        client_socket.close()
        logging.info(f"Connection closed for {client_address}")

def start_server(host: str = '0.0.0.0', port: int = 8888) -> None:
    """Start the server on all available interfaces."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        logging.info(f"Server listening on {host}:{port}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()