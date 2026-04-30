import socket
import ssl
import logging
from typing import Optional

class SecureEchoServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8443):
        self.host = host
        self.port = port
        self.context: Optional[ssl.SSLContext] = None
        self.socket: Optional[socket.socket] = None
        self.logger = logging.getLogger(__name__)

    def setup_ssl_context(self) -> None:
        """Set up SSL context with secure configuration."""
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')

    def start(self) -> None:
        """Start the echo server."""
        try:
            self.setup_ssl_context()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.logger.info(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, addr = self.socket.accept()
                self.handle_client(client_socket, addr)
        except Exception as e:
            self.logger.error(f"Server error: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, addr: tuple) -> None:
        """Handle a client connection."""
        try:
            self.logger.info(f"New connection from {addr[0]}:{addr[1]}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                client_socket.sendall(data)
        except ssl.SSLError as e:
            self.logger.error(f"SSL error with {addr[0]}:{addr[1]}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error handling client {addr[0]}:{addr[1]}: {str(e)}")
        finally:
            client_socket.close()
            self.logger.info(f"Connection closed for {addr[0]}:{addr[1]}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = SecureEchoServer()
    server.start()