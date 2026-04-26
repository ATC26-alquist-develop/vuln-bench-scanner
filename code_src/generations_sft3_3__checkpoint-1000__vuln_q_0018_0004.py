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
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.active_connections: List[Tuple[socket.socket, ssl.SSLSocket]] = []
        
        # Create a secure SSL context
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = True
        self.context.verify_mode = ssl.CERT_REQUIRED
        
        # Set secure defaults
        self.context.options |= (
            ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION
        )

    def create_secure_connection(self) -> Tuple[socket.socket, ssl.SSLSocket]:
        """Create a secure connection to a server."""
        try:
            # Create a new socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap the socket with SSL
            ssl_sock = self.context.wrap_socket(
                sock,
                server_hostname=self.host
            )
            
            # Connect to the server
            ssl_sock.connect((self.host, self.port))
            
            # Add to active connections
            self.active_connections.append((sock, ssl_sock))
            
            logger.info(f"Successfully connected to {self.host}:{self.port}")
            return sock, ssl_sock
            
        except Exception as e:
            logger.error(f"Failed to create connection: {str(e)}")
            return None, None

    def close_connection(self, sock: socket.socket, ssl_sock: ssl.SSLSocket) -> None:
        """Safely close a connection."""
        try:
            # Close the SSL socket
            ssl_sock.close()
            
            # Remove from active connections
            self.active_connections = [
                (s, ssl) for s, ssl in self.active_connections
                if s != sock and ssl != ssl_sock
            ]
            
            logger.info(f"Closed connection to {self.host}:{self.port}")
            
        except Exception as e:
            logger.error(f"Error closing connection: {str(e)}")

    def get_active_connections(self) -> List[Tuple[socket.socket, ssl.SSLSocket]]:
        """Get a copy of active connections."""
        return self.active_connections.copy()

    def cleanup(self) -> None:
        """Safely clean up all connections."""
        for sock, ssl_sock in self.active_connections:
            self.close_connection(sock, ssl_sock)
        self.active_connections.clear()

def main():
    # Example usage
    manager = SecureSocketManager("example.com", 443)
    
    try:
        # Create multiple connections
        for _ in range(5):
            sock, ssl_sock = manager.create_secure_connection()
            if sock and ssl_sock:
                # Use the connection...
                pass
                
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        
    finally:
        # Clean up all connections
        manager.cleanup()

if __name__ == "__main__":
    main()