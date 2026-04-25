import socket
import ssl
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureTCPServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8443):
        self.host = host
        self.port = port
        self.context = self._create_ssl_context()
        self.socket = None

    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create a secure SSL context with strong security settings."""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        return context

    def start(self):
        """Start the secure TCP server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            logger.info(f"Server started on {self.host}:{self.port}")

            while True:
                client_socket, addr = self.socket.accept()
                self._handle_client(client_socket, addr)
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
        finally:
            self._cleanup()

    def _handle_client(self, client_socket: ssl.SSLSocket, addr: Tuple[str, int]):
        """Handle a client connection securely."""
        try:
            logger.info(f"New connection from {addr}")
            with client_socket:
                # Implement your secure communication logic here
                pass
        except ssl.SSLError as e:
            logger.error(f"SSL error with {addr}: {str(e)}")
        except Exception as e:
            logger.error(f"Error handling client {addr}: {str(e)}")
        finally:
            client_socket.close()

    def _cleanup(self):
        """Clean up resources."""
        if self.socket:
            self.socket.close()
        logger.info("Server stopped")

if __name__ == "__main__":
    server = SecureTCPServer()
    server.start()