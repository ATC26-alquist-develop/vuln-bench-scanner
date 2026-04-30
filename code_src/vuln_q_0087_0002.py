```python
import socket
import ssl
import secrets
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')  # Strong cipher suite
        self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)
                logger.info(f"Server listening on {self.host}:{self.port}")
                
                with self.context.wrap_socket(server_socket, server_side=True) as secure_socket:
                    while True:
                        try:
                            client_socket, addr = secure_socket.accept()
                            logger.info(f"Accepted connection from {addr}")
                            self.handle_client(client_socket, addr)
                        except ssl.SSLError as e:
                            logger.error(f"SSL error: {e}")
                        except Exception as e:
                            logger.error(f"Error handling client: {e}")
            except Exception as e:
                logger.error(f"Server error: {e}")

    def handle_client(self, client_socket: ssl.SSLSocket, addr: Tuple[str, int]):
        try:
            # Implement secure client handling here
            pass
        finally:
            client_socket.close()

class SecureClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = True
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.load_verify_locations("server.crt")

    def connect(self):
        with socket.create_connection((self.host, self.port)) as sock:
            with self.context.wrap_socket(sock, server_hostname=self.host) as secure_sock:
                logger.info(f"Connected to {self.host}:{self.port}")
                # Implement secure communication here

def main():
    # Example usage
    server = SecureServer('127.0.0.1', 8443)
    server.start()

if __name__ == "__main__":
    main()
```