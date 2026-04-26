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

def bind_socket(sock: socket.socket, host: str = '0.0.0.0', port: int = 8888) -> None:
    """Bind the socket to the specified host and port."""
    try:
        sock.bind((host, port))
        sock.listen(5)
        logging.info(f"Listening on {host}:{port}")
    except socket.error as e:
        logging.error(f"Failed to bind socket: {e}")
        raise

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
    except socket.error as e:
        logging.error(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Connection closed for {client_address}")

def main() -> None:
    """Main function to run the server."""
    try:
        sock = create_secure_socket()
        bind_socket(sock)
        
        while True:
            client_socket, client_address = sock.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        logging.info("Server shutting down")
    finally:
        if 'sock' in locals():
            sock.close()

if __name__ == "__main__":
    main()