import socket
import ssl
import logging
from typing import Tuple
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocketServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 65432):
        self.host = host
        self.port = port
        self.context = self._create_secure_context()
        self.socket = None

    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context with strong security settings."""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        return context

    def start(self):
        """Start the secure server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            logger.info(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, addr = self.socket.accept()
                logger.info(f"Accepted connection from {addr}")
                self._handle_client(client_socket, addr)
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
        finally:
            self._cleanup()

    def _handle_client(self, client_socket: ssl.SSLSocket, addr: Tuple[str, int]):
        """Handle client connection securely."""
        try:
            # Verify client certificate
            cert = client_socket.getpeercert(binary_form=True)
            if not cert:
                logger.warning(f"No certificate from {addr}")
                client_socket.close()
                return

            # Verify certificate
            self.context.verify_mode = ssl.CERT_REQUIRED
            self.context.check_hostname = True
            self.context.verify_flags = ssl.VERIFY_X509_STRICT

            # Wrap socket with SSL
            secure_socket = self.context.wrap_socket(client_socket, server_side=True)
            secure_socket.do_handshake()

            # Process client data securely
            data = secure_socket.recv(1024)
            if not data:
                logger.warning(f"Empty data received from {addr}")
                secure_socket.close()
                return

            # Process data (implement your logic here)
            response = f"Received: {data.decode('utf-8')}"
            secure_socket.send(response.encode('utf-8'))

        except ssl.SSLCertVerificationError as e:
            logger.error(f"Certificate verification failed: {str(e)}")
        except ssl.SSLError as e:
            logger.error(f"SSL error: {str(e)}")
        except Exception as e:
            logger.error(f"Error handling client {addr}: {str(e)}")
        finally:
            secure_socket.close()

    def _cleanup(self):
        """Clean up resources."""
        if self.socket:
            self.socket.close()
        logger.info("Server stopped")

def main():
    server = SecureSocketServer()
    try:
        server.start()
    except KeyboardInterrupt:
        logger.info("Server shutting down")
    finally:
        server._cleanup()

if __name__ == "__main__":
    main()