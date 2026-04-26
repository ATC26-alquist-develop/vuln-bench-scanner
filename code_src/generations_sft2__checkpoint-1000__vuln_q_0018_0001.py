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
        self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        self.context.options |= ssl.OP_NO_TLSv1_3_COMPAT  # Disable TLS 1.3 compatibility

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            logger.info(f"Server listening on {self.host}:{self.port}")

            with self.context.wrap_socket(server_socket, server_side=True) as secure_socket:
                while True:
                    try:
                        client_socket, addr = secure_socket.accept()
                        logger.info(f"New connection from {addr}")
                        self.handle_client(client_socket, addr)
                    except ssl.SSLError as e:
                        logger.error(f"SSL error: {e}")
                    except Exception as e:
                        logger.error(f"Error accepting connection: {e}")

    def handle_client(self, client_socket: ssl.SSLSocket, addr: Tuple[str, int]):
        try:
            # Generate a secure random token for each session
            session_token = secrets.token_hex(32)
            
            # Send token to client
            client_socket.sendall(f"Session token: {session_token}".encode('utf-8'))
            
            # Receive data from client
            data = client_socket.recv(1024).decode('utf-8')
            
            # Process data (example: echo back)
            response = f"Server received: {data}"
            client_socket.sendall(response.encode('utf-8'))
            
            logger.info(f"Connection closed with {addr}")
        except Exception as e:
            logger.error(f"Error handling client {addr}: {e}")
        finally:
            client_socket.close()

class SecureClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_verify_locations("server.crt")
        self.context.check_hostname = True
        self.context.verify_mode = ssl.CERT_REQUIRED

    def connect(self):
        with socket.create_connection((self.host, self.port)) as sock:
            with self.context.wrap_socket(sock, server_hostname=self.host) as secure_sock:
                logger.info(f"Connected to {self.host}:{self.port}")
                return secure_sock

    def send_data(self, secure_sock: ssl.SSLSocket, data: str):
        try:
            secure_sock.sendall(data.encode('utf-8'))
            response = secure_sock.recv(1024).decode('utf-8')
            logger.info(f"Received: {response}")
        except Exception as e:
            logger.error(f"Error sending/receiving data: {e}")

# Usage example
if __name__ == "__main__":
    # Server
    server = SecureServer('localhost', 8443)
    server.start()

    # Client
    client = SecureClient('localhost', 8443)
    secure_sock = client.connect()
    client.send