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
        """Initialize with SSL certificate and key"""
        self.cert_path = cert_path
        self.key_path = key_path
        self.context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH,
            cafile=cert_path
        )
        self.context.load_cert_chain(certfile=cert_path, keyfile=key_path)
        
    def connect(self, host: str, port: int) -> ssl.SSLSocket:
        """Establish secure connection to server"""
        try:
            sock = socket.create_connection((host, port), timeout=self.timeout)
            secure_sock = self.context.wrap_socket(
                sock,
                server_hostname=host
            )
            logging.info(f"Connected to {host}:{port}")
            return secure_sock
        except (socket.error, ssl.SSLError) as e:
            logging.error(f"Connection failed: {e}")
            raise

    def disconnect(self, sock: ssl.SSLSocket) -> None:
        """Safely close connection"""
        try:
            sock.close()
            logging.info("Connection closed")
        except socket.error as e:
            logging.error(f"Error closing connection: {e}")

def main():
    """Main function with secure socket connections"""
    # Configuration (should be stored securely, not hardcoded)
    servers = [
        ServerConfig("example.com", 443),
        ServerConfig("api.example.org", 443)
    ]
    
    # Initialize SSL context with proper certificate
    manager = SecureSocketManager(
        cert_path="/path/to/valid/certificate.pem",
        key_path="/path/to/valid/private_key.pem"
    )

    try:
        for server in servers:
            try:
                with manager.connect(server.hostname, server.port) as conn:
                    # Perform operations here
                    logging.info(f"Successfully connected to {server.hostname}:{server.port}")
            except Exception as e:
                logging.error(f"Failed to connect to {server.hostname}:{server.port}: {e}")
    except Exception as e:
        logging.error(f"Error in main: {e}")
    finally:
        # Ensure all connections are properly closed
        manager.disconnect(conn)

if __name__ == "__main__":
    main()