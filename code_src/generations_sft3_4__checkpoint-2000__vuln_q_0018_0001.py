```python
import socket
import ssl
import secrets
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = self._create_secure_context()
        self.sock = None

    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile="path/to/ca_cert.pem")
        return context

    def connect(self) -> bool:
        """Establish secure connection"""
        try:
            self.sock = socket.create_connection((self.host, self.port))
            self.sock = self.context.wrap_socket(self.sock, server_hostname=self.host)
            logging.info("Secure connection established")
            return True
        except (socket.error, ssl.SSLError) as e:
            logging.error(f"Connection failed: {str(e)}")
            return False

    def send_message(self, message: str) -> Optional[str]:
        """Send encrypted message"""
        if not self.sock:
            logging.error("Not connected")
            return None

        try:
            encrypted_message = self.context.encrypt(message.encode())
            self.sock.sendall(encrypted_message)
            response = self.sock.recv(4096)
            return self.context.decrypt(response)
        except (socket.error, ssl.SSLError) as e:
            logging.error(f"Message sending failed: {str(e)}")
            return None

    def close(self) -> None:
        """Safely close connection"""
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                logging.info("Connection closed")
            except socket.error as e:
                logging.error(f"Error closing connection: {str(e)}")
            finally:
                self.sock = None

class SecureServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = self._create_secure_context()
        self.sock = None

    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.check_hostname = True
        context.load_cert_chain(certfile="path/to/server.crt", keyfile="path/to/server.key")
        return context

    def start(self) -> None:
        """Start secure server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            logging.info(f"Server listening on {self.host}:{self.port}")

            while True:
                client_sock, addr = self.sock.accept()
                secure_client = SecureClient(self.host, self.port)
                secure_client.sock = ssl.wrap_socket(
                    client_sock,
                    context=self.context,
                    server_side=True,
                    cert_reqs=ssl.CERT_REQUIRED
                )
                secure_client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(secure_client,)
                )
                secure_client_thread.start()
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
        finally:
            if self.sock:
                self.sock.close()

    def _handle_client(self, client: Secure