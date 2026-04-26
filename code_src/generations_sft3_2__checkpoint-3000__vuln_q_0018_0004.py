import socket
import ssl
import logging
from typing import List, Tuple
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class ServerConfig:
    """Secure server configuration"""
    hostname: str
    port: int
    timeout: float = 5.0

class SecureSocketManager:
    """Secure socket connection manager"""
    
    def __init__(self, cert_path: str, key_path: str):
        """Initialize with SSL certificates"""
        if not cert_path or not key_path:
            raise ValueError("Certificate and key paths must be provided")
        self.cert_path = cert_path
        self.key_path = key_path
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_cert_chain(certfile=self.cert_path, keyfile=self.key_path)

    def create_secure_connection(self, server_config: ServerConfig) -> ssl.SSLSocket:
        """Create secure socket connection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(server_config.timeout)
            
            # Wrap socket with SSL
            secure_sock = self.context.wrap_socket(
                sock,
                server_hostname=server_config.hostname
            )
            
            # Perform connection
            secure_sock.connect((server_config.hostname, server_config.port))
            logging.info(f"Secure connection established to {server_config.hostname}")
            return secure_sock
            
        except (socket.timeout, ssl.SSLError, socket.error) as e:
            logging.error(f"Connection failed: {str(e)}")
            raise

    def create_connections(self, server_configs: List[ServerConfig]) -> List[ssl.SSLSocket]:
        """Create multiple secure connections"""
        if not server_configs:
            raise ValueError("At least one server configuration required")
            
        connections = []
        for config in server_configs:
            if not isinstance(config, ServerConfig):
                raise TypeError("Invalid server configuration type")
            connections.append(self.create_secure_connection(config))
            
        return connections

def main():
    """Main function with secure example usage"""
    try:
        # Initialize with valid paths
        cert_path = "/path/to/valid/cert.pem"
        key_path = "/path/to/valid/key.pem"
        manager = SecureSocketManager(cert_path, key_path)
        
        # Example server configurations
        servers = [
            ServerConfig("example.com", 443),
            ServerConfig("api.example.com", 443),
            ServerConfig("secure.example.org", 443)
        ]
        
        # Create connections
        connections = manager.create_connections(servers)
        
        # Use connections securely
        for conn in connections:
            try:
                # Perform secure operations here
                conn.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
                response = conn.recv(1024)
                logging.info(f"Received response: {response[:100]}...")
                
            except Exception as e:
                logging.error(f"Error processing connection: {str(e)}")
            finally:
                conn.close()
                
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()