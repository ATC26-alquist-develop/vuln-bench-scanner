```python
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
    cert_path: str
    key_path: str

class SecureSocketManager:
    """Secure implementation of multiple socket connections"""
    
    def __init__(self, server_configs: List[ServerConfig]):
        """Initialize with list of server configurations"""
        self.servers = []
        self.ssl_context = self._create_ssl_context()
        
        for config in server_configs:
            self.servers.append(self._create_secure_connection(config))
            
    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile="/path/to/ca_cert.pem")
        return context

    def _create_secure_connection(self, config: ServerConfig) -> ssl.SSLSocket:
        """Create secure socket connection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_sock = self.ssl_context.wrap_socket(sock, server_hostname=config.hostname)
            
            # Set timeout to prevent hanging connections
            ssl_sock.settimeout(30)
            
            # Connect to server
            ssl_sock.connect((config.hostname, config.port))
            
            logger.info(f"Successfully connected to {config.hostname}:{config.port}")
            return ssl_sock
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Failed to connect to {config.hostname}:{config.port}: {str(e)}")
            raise

    def send_data(self, data: bytes, server_index: int) -> None:
        """Send data to a specific server"""
        if server_index < 0 or server_index >= len(self.servers):
            logger.error("Invalid server index")
            return
            
        try:
            self.servers[server_index].sendall(data)
            logger.info(f"Sent data to server {server_index}")
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Failed to send data to server {server_index}: {str(e)}")
            raise

    def receive_data(self, server_index: int, max_size: int = 1024) -> bytes:
        """Receive data from a specific server"""
        if server_index < 0 or server_index >= len(self.servers):
            logger.error("Invalid server index")
            return b""
            
        try:
            data = self.servers[server_index].recv(max_size)
            logger.info(f"Received data from server {server_index}")
            return data
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Failed to receive data from server {server_index}: {str(e)}")
            raise

    def close_all_connections(self) -> None:
        """Close all connections"""
        for server in self.servers:
            try:
                server.close()
                logger.info("Closed connection to server")
            except (socket.error, ssl.SSLError) as e:
                logger.error(f"Failed to close connection to server: {str(e)}")
                raise

# Example usage
if __name__ == "__main__":
    # List of server configurations
    server_configs = [
        ServerConfig("example.com", 443, "/path/to/example.com.crt", "/path/to/example.com.key"),
        ServerConfig("example.org", 443, "/path/to/example.org.crt", "/path/to/example.org.key")
    ]
    
    try:
        manager = SecureSocketManager(server_configs)
        
        # Example usage