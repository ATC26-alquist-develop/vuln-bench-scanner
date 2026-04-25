import socket
import ssl
import logging
from typing import Optional

class SecureNetworkMonitor:
    def __init__(self, host: str, port: int, timeout: int = 5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def check_server(self) -> bool:
        try:
            # Create a secure SSL context
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED

            # Create a secure socket
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=self.host) as secure_sock:
                    self.logger.info(f"Successfully connected to {self.host}:{self.port}")
                    return True
        except (socket.timeout, ssl.SSLCertVerificationError, socket.error) as e:
            self.logger.error(f"Failed to connect to {self.host}:{self.port}: {str(e)}")
            return False

    def __str__(self) -> str:
        return f"SecureNetworkMonitor(host={self.host}, port={self.port}, timeout={self.timeout})"

if __name__ == "__main__":
    monitor = SecureNetworkMonitor("example.com", 443)
    print(monitor)
    print("Server status:", "Available" if monitor.check_server() else "Not available")