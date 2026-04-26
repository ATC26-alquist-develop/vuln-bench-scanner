```python
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
        self.sock = None

    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_verify_locations(cafile="/path/to/ca_cert.pem")
        return context

    def connect(self) -> None:
        """Establish secure connection"""
        try:
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            self.sock = self.context.wrap_socket(sock, server_hostname=self.host)
            
            # Connect
            self.sock.connect((self.host, self.port))
            logger.info("Secure connection established")
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            self.close()
            raise

    def send(self, data: str) -> None:
        """Send data securely"""
        if not self.sock:
            raise ConnectionError("Not connected")
            
        try:
            # Encode and send data
            self.sock.sendall(data.encode('utf-8'))
        except Exception as e:
            logger.error(f"Send failed: {str(e)}")
            self.close()
            raise

    def receive(self, max_size: int = 1024) -> str:
        """Receive data securely"""
        if not self.sock:
            raise ConnectionError("Not connected")
            
        try:
            # Receive data
            data = self.sock.recv(max_size)
            if not data:
                raise ConnectionError("Connection closed")
            return data.decode('utf-8')
        except Exception as e:
            logger.error(f"Receive failed: {str(e)}")
            self.close()
            raise

    def close(self) -> None:
        """Safely close connection"""
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
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
        context.load_cert_chain(certfile="/path/to/cert.pem", keyfile="/path/to/key.pem")
        return context

    def start(self) -> None:
        """Start secure server"""
        try:
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Bind
            sock.bind((self.host, self.port))
            
            # Listen
            sock.listen(5)
            
            while True:
                # Accept connection
                client_sock, address = sock.accept()
                client = SecureClient(client_sock, address)
                client_thread = threading.Thread(target=self._handle_client, args=(client,))
                client_thread.start()
        except Exception as e:
            logger.error(f"Server start failed: {str(e)}")
            self.close()
            raise

    def _handle_client(self, client: SecureClient) -> None:
        """Handle client connection"""
        try:
            # Example