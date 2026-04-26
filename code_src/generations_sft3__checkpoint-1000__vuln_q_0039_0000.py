import socket
import threading
import logging
from typing import Tuple
from ipaddress import ip_address

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 8888):
        """Initialize secure server with proper configuration."""
        # Validate and sanitize host
        try:
            self.host = str(ip_address(host))
        except ValueError:
            raise ValueError("Invalid host address")
        
        # Validate and sanitize port
        if not (1024 <= port <= 65535):
            raise ValueError("Port must be between 1024 and 65535")
        
        self.port = port
        self.socket = None
        self.running = False

    def start(self):
        """Start the secure server."""
        try:
            # Create socket with proper options
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to localhost only
            self.socket.bind((self.host, self.port))
            
            # Listen with proper backlog
            self.socket.listen(5)
            self.running = True
            
            logger.info(f"Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.start()
                except socket.error as e:
                    logger.error(f"Socket error: {e}")
                    break
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            self.stop()

    def stop(self):
        """Safely stop the server."""
        self.running = False
        if self.socket:
            self.socket.close()
        logger.info("Server stopped")

    def handle_client(self, client_socket: socket.socket, address: Tuple[str, int]):
        """Handle client connections securely."""
        try:
            # Set timeout for client connections
            client_socket.settimeout(30)
            
            # Receive data with proper buffer size
            data = client_socket.recv(1024)
            
            if data:
                # Process received data (implement your logic here)
                response = "Server received: " + data.decode('utf-8')
                client_socket.send(response.encode('utf-8'))
            
        except socket.timeout:
            logger.warning(f"Client {address} timed out")
        except Exception as e:
            logger.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = SecureServer()
    try:
        server.start()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        server.stop()