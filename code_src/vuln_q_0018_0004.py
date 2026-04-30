import socket
import ssl
import logging
from typing import List, Tuple
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocketClient:
    def __init__(self, host: str, port: int, timeout: int = 10):
        """Initialize secure socket client with TLS."""
        self.host = host
        self.port = port
        self.timeout = timeout
        self.context = ssl.create_default_context()
        self.context.check_hostname = True
        self.context.verify_mode = ssl.CERT_REQUIRED

    @contextmanager
    def secure_connection(self):
        """Establish secure TLS connection with timeout."""
        sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        try:
            with self.context.wrap_socket(sock, server_hostname=self.host) as secure_sock:
                yield secure_sock
        except (socket.timeout, ssl.SSLCertVerificationError, 
                ssl.SSLCertError, ssl.SSLError) as e:
            logger.error(f"Connection error: {type(e).__name__}")
            raise
        finally:
            sock.close()

    def send_receive(self, data: bytes) -> Tuple[bool, bytes]:
        """Send data and receive response securely."""
        try:
            with self.secure_connection() as secure_sock:
                secure_sock.sendall(data)
                response = secure_sock.recv(4096)
            return True, response
        except Exception as e:
            logger.error(f"Communication error: {type(e).__name__}")
            return False, b''

def main():
    """Main function to demonstrate secure socket usage."""
    servers = [
        ("example.com", 443),
        ("api.example.com", 443),
        ("secure.example.com", 443)
    ]

    for host, port in servers:
        client = SecureSocketClient(host, port)
        try:
            success, response = client.send_receive(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
            if success:
                logger.info(f"Successfully connected to {host}:{port}")
                logger.info(f"Received response: {response.decode()}")
            else:
                logger.warning(f"Failed to connect to {host}:{port}")
        except Exception as e:
            logger.error(f"Error processing {host}:{port}: {type(e).__name__}")

if __name__ == "__main__":
    main()