import socket
import threading
import logging
from typing import Tuple
from ipaddress import ip_address

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureLocalServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None
        
    def start(self):
        try:
            # Create a socket with IPV6 support
            self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            
            # Bind to all interfaces
            self.socket.bind((self.host, self.port))
            
            # Listen for connections
            self.socket.listen(5)
            
            logger.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client, address = self.socket.accept()
                threading.Thread(target=self.handle_client, args=(client, address)).start()
                
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()
    
    def handle_client(self, client_socket: socket.socket, address: Tuple[str, int]):
        try:
            # Handle client connection securely
            logger.info(f"New connection from {address}")
            # Add your secure handling logic here
            
        except Exception as e:
            logger.error(f"Error handling client {address}: {str(e)}")
        finally:
            client_socket.close()

# Usage example
if __name__ == "__main__":
    server = SecureLocalServer("fe80::1%lo0", 8000)
    server.start()