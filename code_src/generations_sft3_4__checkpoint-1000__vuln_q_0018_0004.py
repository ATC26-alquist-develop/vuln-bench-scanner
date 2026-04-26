import socket
import ssl
import logging
from typing import List, Tuple
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocketManager:
    def __init__(self, host: str, port: int, max_connections: int = 5):
        """
        Initialize secure socket manager with proper security controls.
        
        Args:
            host: Target server hostname
            port: Target server port
            max_connections: Maximum number of concurrent connections
        """
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.active_connections: List[Tuple[socket.socket, ssl.SSLSocket]] = []
        
        # Create secure SSL context
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.ssl_context.check_hostname = True
        self.ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        # Set secure timeout
        self.timeout = 5.0

    def connect(self) -> None:
        """
        Establish a secure connection to the target server.
        """
        try:
            # Create a secure socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # Wrap socket with SSL
            ssl_sock = self.ssl_context.wrap_socket(
                sock,
                server_hostname=self.host
            )
            
            # Establish connection
            ssl_sock.connect((self.host, self.port))
            
            # Add connection to active connections
            self.active_connections.append((sock, ssl_sock))
            
            logger.info(f"Successfully connected to {self.host}:{self.port}")
            
        except ssl.SSLError as e:
            logger.error(f"SSL error: {e}")
        except socket.error as e:
            logger.error(f"Socket error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def disconnect(self) -> None:
        """
        Safely disconnect from the target server.
        """
        try:
            for sock, ssl_sock in self.active_connections:
                try:
                    ssl_sock.close()
                    sock.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {e}")
            self.active_connections.clear()
            logger.info("Disconnected from server")
            
        except Exception as e:
            logger.error(f"Error during disconnection: {e}")

    def get_active_connections(self) -> List[Tuple[socket.socket, ssl.SSLSocket]]:
        """
        Get a copy of active connections for safe handling.
        """
        return self.active_connections.copy()

def main():
    # Example usage
    try:
        manager = SecureSocketManager("example.com", 443)
        
        # Establish connections
        for _ in range(5):
            manager.connect()
        
        # Wait for connections to be established
        import time
        time.sleep(2)
        
        # Get active connections
        active = manager.get_active_connections()
        logger.info(f"Active connections: {active}")
        
        # Disconnect
        manager.disconnect()
        
    except Exception as e:
        logger.error(f"Main execution error: {e}")

if __name__ == "__main__":
    main()