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
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            # Wrap socket with SSL
            ssl_socket = self.context.wrap_socket(
                server_socket,
                server_side=True,
                do_handshake_on_connect=True
            )
            
            logger.info(f"Secure server started on {self.host}:{self.port}")
            return ssl_socket, self.context
            
        except Exception as e:
            logger.error(f"Error starting server: {str(e)}")
            raise

    def start_client(self) -> Tuple[ssl.SSLSocket, ssl.SSLContext]:
        """Start secure client"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_socket = self.context.wrap_socket(
                client_socket,
                server_hostname=self.host,
                do_handshake_on_connect=True
            )
            
            ssl_socket.connect((self.host, self.port))
            logger.info(f"Secure client connected to {self.host}:{self.port}")
            return ssl_socket, self.context
            
        except Exception as e:
            logger.error(f"Error starting client: {str(e)}")
            raise

def main():
    # Example usage
    try:
        # Server setup
        server = SecureSocket('localhost', 8443, 'server.crt', 'server.key')
        server_socket, ssl_context = server.start_server()
        
        # Client setup
        client_socket, ssl_context = server.start_client()
        
        # Simple communication
        message = "Hello from client"
        client_socket.send(message.encode())
        response = client_socket.recv(1024)
        print(f"Received: {response.decode()}")
        
    except Exception as e:
        logger.error(f"Communication error: {str(e)}")
    finally:
        # Cleanup
        if 'server_socket' in locals():
            server_socket.close()
        if 'client_socket' in locals():
            client_socket.close()

if __name__ == "__main__":
    main()