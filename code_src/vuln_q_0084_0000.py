import socket
import sys
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_and_close_socket(host: str = 'localhost', port: int = 12345) -> None:
    """
    Creates a socket connection to the specified host and port, then closes it.
    
    Args:
        host (str): The hostname or IP address to connect to. Defaults to 'localhost'.
        port (int): The port number to connect to. Defaults to 12345.
    """
    try:
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            logging.info(f"Attempting to connect to {host}:{port}")
            
            # Set a timeout for the connection attempt
            s.settimeout(5)
            
            # Attempt to connect
            try:
                s.connect((host, port))
                logging.info(f"Successfully connected to {host}:{port}")
                
                # Send a test message
                s.sendall(b"Hello, server!")
                
                # Receive response (if any)
                data = s.recv(1024)
                logging.info(f"Received: {data.decode('utf-8')}")
                
            except socket.timeout:
                logging.error(f"Connection to {host}:{port} timed out")
            except socket.error as e:
                logging.error(f"Error connecting to {host}:{port}: {e}")
            finally:
                # Ensure the socket is closed
                s.close()
                logging.info(f"Socket closed")
                
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_and_close_socket()