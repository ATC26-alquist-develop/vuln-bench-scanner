import socket
import ssl
import logging
from typing import List, Tuple
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ServerConfig:
    """Secure configuration for each server"""
    hostname: str
    port: int
    ca_cert_path: str
    cert_path: str
    key_path: str

class SecureSocketManager:
    """Secure implementation for managing multiple socket connections"""
    
    def __init__(self, server_configs: List[ServerConfig]):
        """Initialize with list of server configurations"""
        self.server_configs = server_configs
        self.connections: List[Tuple[socket.socket, ssl.SSLSocket]] = []

    def create_secure_connection(self, server_config: ServerConfig) -> Tuple[socket.socket, ssl.SSLSocket]:
        """Create a secure connection to a server"""
        try:
            # Create a secure SSL context
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_verify_locations(cafile=server_config.ca_cert_path)
            context.load_cert_chain(certfile=server_config.cert_path, keyfile=server_config.key_path)
            
            # Create a socket and wrap it with SSL
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_sock = context.wrap_socket(sock, server_hostname=server_config.hostname)
            
            # Connect to the server
            ssl_sock.connect((server_config.hostname, server_config.port))
            
            # Add connection to list
            self.connections.append((sock, ssl_sock))
            
            logger.info(f"Successfully connected to {server_config.hostname}:{server_config.port}")
            return ssl_sock
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Failed to connect to {server_config.hostname}:{server_config.port}: {str(e)}")
            return None

    def close_connections(self):
        """Safely close all connections"""
        for sock, ssl_sock in self.connections:
            try:
                ssl_sock.close()
                sock.close()
            except Exception as e:
                logger.error(f"Error closing connection: {str(e)}")
        self.connections.clear()

    def get_active_connections(self) -> List[Tuple[socket.socket, ssl.SSLSocket]]:
        """Get list of active connections"""
        return self.connections

# Example usage
if __name__ == "__main__":
    # Example server configurations
    server_configs = [
        ServerConfig(
            hostname="example.com",
            port=443,
            ca_cert_path="/path/to/ca_cert.pem",
            cert_path="/path/to/client_cert.pem",
            key_path="/path/to/client_key.pem"
        )
    ]
    
    manager = SecureSocketManager(server_configs)
    
    # Create connections
    for config in server_configs:
        connection = manager.create_secure_connection(config)
        if connection:
            print(f"Connected to {config.hostname}:{config.port}")
    
    # Simulate some work
    import time
    time.sleep(5)
    
    # Close connections
    manager.close_connections()