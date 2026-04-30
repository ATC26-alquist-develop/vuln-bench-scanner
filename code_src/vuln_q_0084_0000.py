```python
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
```


This implementation includes several security and best practices:

1. We use a context manager (`with` statement) to ensure the socket is always closed, even if an exception occurs.
2. We set a timeout for the connection attempt to prevent hanging.
3. We use logging to provide clear information about the connection process and any errors.
4. We handle exceptions to prevent crashes and provide meaningful error messages.
5. We use type hints to improve code readability and catch potential type-related errors.
6. We don't expose sensitive information in error messages.
7. We use a constant port number (12345) as per the user's request, which is safe for testing purposes.

This code creates a socket connection, sends a test message, receives a response (if any), and then properly closes the connection. It's designed to be secure and robust, following Python best practices and security guidelines.