import socket
import ssl
import secrets
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = self._create_secure_context()
        
    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile="/path/to/ca_cert.pem")
        return context

    def connect(self) -> ssl.SSLSocket:
        """Establish secure connection"""
        try:
            sock = socket.create_connection((self.host, self.port))
            secure_sock = self.context.wrap_socket(sock, server_hostname=self.host)
            return secure_sock
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Connection error: {e}")
            raise

class SecureServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = self._create_secure_context()
        
    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_cert_chain(certfile="/path/to/cert.pem", keyfile="/path/to/key.pem")
        return context

    def start(self) -> None:
        """Start secure server"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            logger.info(f"Server listening on {self.host}:{self.port}")
            
            while True:
                try:
                    client_socket, addr = server_socket.accept()
                    with self.context.wrap_socket(client_socket, server_side=True) as secure_socket:
                        logger.info(f"Secure connection from {addr}")
                        # Handle secure communication with client
                except ssl.SSLError as e:
                    logger.error(f"SSL error: {e}")
                except Exception as e:
                    logger.error(f"Error accepting connection: {e}")

def main():
    # Example usage
    try:
        # Server
        server = SecureServer('localhost', 8443)
        server.start()
        
        # Client
        client = SecureClient('localhost', 8443)
        with client.connect() as secure_sock:
            # Perform secure communication
            pass
            
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()