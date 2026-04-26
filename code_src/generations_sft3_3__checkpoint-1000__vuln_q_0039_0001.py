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
        # Send a simple response
        client_socket.sendall(b"Connection established\n")
        # Receive data from client (max 1024 bytes)
        data = client_socket.recv(1024)
        if data:
            logging.info(f"Received data from {client_address}: {data.decode('utf-8')}")
        # Close the connection
        client_socket.close()
    except Exception as e:
        logging.error(f"Error handling client {client_address}: {str(e)}")

def main() -> None:
    """Main function to set up and run the server."""
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set SO_REUSEADDR to allow reuse of local addresses
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to all available interfaces
        server_socket.bind(('0.0.0.0', 8888))
        
        # Listen for incoming connections
        server_socket.listen(5)
        
        logging.info("Server started. Waiting for connections...")
        
        while True:
            try:
                # Accept a new connection
                client_socket, client_address = server_socket.accept()
                
                # Start a new thread to handle the client
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()
            except socket.error as e:
                logging.error(f"Socket error: {str(e)}")
                break
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
    finally:
        # Clean up
        if 'server_socket' in locals():
            server_socket.close()

if __name__ == "__main__":
    main()