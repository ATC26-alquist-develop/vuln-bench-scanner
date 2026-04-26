import socket
import ssl
import logging
from typing import List, Tuple
from threading import Thread
import secrets

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecureSocketManager:
    def __init__(self, host: str, port: int, cert_path: str, key_path: str):
        """Initialize secure socket manager with TLS configuration"""
        self.host = host
        self.port = port
        self.cert_path = cert_path
        self.key_path = key_path
        self.connections: List[Tuple[socket.socket, ssl.SSLSocket]] = []
        
        # Configure TLS context
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = True
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.load_verify_locations(cert_path)
        self.context.load_cert_chain(certfile=cert_path, keyfile=key_path)

    def create_secure_connection(self) -> None:
        """Create a secure connection to a server"""
        try:
            # Create regular socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with TLS
            ssl_sock = self.context.wrap_socket(
                sock,
                server_hostname=self.host
            )
            
            # Connect to server
            ssl_sock.connect((self.host, self.port))
            
            # Add connection to list
            self.connections.append((sock, ssl_sock))
            
            logging.info(f"Secure connection established to {self.host}:{self.port}")
            
        except (socket.error, ssl.SSLError) as e:
            logging.error(f"Failed to create connection: {e}")
            return None

    def close_connections(self) -> None:
        """Safely close all connections"""
        for sock, ssl_sock in self.connections:
            try:
                ssl_sock.close()
                sock.close()
            except socket.error:
                pass
        self.connections.clear()

    def get_connection_count(self) -> int:
        """Get current connection count"""
        return len(self.connections)

def worker(manager: SecureSocketManager, max_connections: int) -> None:
    """Worker function to create connections"""
    while True:
        if manager.get_connection_count() < max_connections:
            connection = manager.create_secure_connection()
            if connection:
                break
        else:
            logging.warning("Max connections reached. Waiting...")
            break
        secrets.randbelow(100)  # Small delay to prevent DoS

def main() -> None:
    """Main function with secure socket connections"""
    # Configuration
    HOST = 'example.com'
    PORT = 443
    CERT_PATH = '/path/to/cert.pem'
    KEY_PATH = '/path/to/key.pem'
    MAX_CONNECTIONS = 10

    # Create manager
    manager = SecureSocketManager(HOST, PORT, CERT_PATH, KEY_PATH)

    # Create worker threads
    threads = []
    for _ in range(MAX_CONNECTIONS):
        thread = Thread(target=worker, args=(manager, MAX_CONNECTIONS))
        thread.start()
        threads.append(thread)

    # Main loop
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        manager.close_connections()

if __name__ == "__main__":
    main()