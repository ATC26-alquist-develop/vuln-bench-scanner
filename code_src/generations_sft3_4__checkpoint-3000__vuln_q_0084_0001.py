import socket
import ssl
import secrets
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocket:
    def __init__(self, host: str, port: int, cert_path: str, key_path: str):
        """Initialize secure socket with TLS"""
        self.host = host
        self.port = port
        self.cert_path = cert_path
        self.key_path = key_path
        self.context = self._create_secure_context()
        
    def _create_secure_context(self) -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.cert_path, keyfile=self.key_path)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        return context

    def start_server(self) -> Tuple[socket.socket, ssl.SSLContext]:
        """Start secure server"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((self.host, self.port))
                sock.listen(5)
                client_socket, address = sock.accept()
                
                # Wrap socket with SSL
                secure_socket = self.context.wrap_socket(client_socket, server_side=True)
                
                logger.info(f"Secure server started on {self.host}:{self.port}")
                return secure_socket, address
        except Exception as e:
            logger.error(f"Error starting server: {str(e)}")
            raise

    def start_client(self) -> Tuple[socket.socket, ssl.SSLContext]:
        """Start secure client"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)  # Set timeout to prevent hanging
                secure_socket = self.context.wrap_socket(sock, server_hostname=self.host)
                
                secure_socket.connect((self.host, self.port))
                logger.info(f"Secure client connected to {self.host}:{self.port}")
                return secure_socket, None
        except Exception as e:
            logger.error(f"Error starting client: {str(e)}")
            raise

def main():
    # Example usage
    try:
        # Server setup
        server = SecureSocket('localhost', 8443, 'server.crt', 'server.key')
        server_socket, address = server.start_server()
        
        # Handle server connection
        while True:
            data = server_socket.recv(1024)
            if not data:
                break
            # Process data...
            server_socket.sendall(b"Received")
            
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
    
    try:
        # Client setup
        client = SecureSocket('localhost', 8443, 'client.crt', 'client.key')
        client_socket, address = client.start_client()
        
        # Handle client connection
        client_socket.sendall(b"Hello Server")
        data = client_socket.recv(1024)
        print(f"Received: {data.decode()}")
        
    except Exception as e:
        logger.error(f"Client error: {str(e)}")

if __name__ == "__main__":
    main()