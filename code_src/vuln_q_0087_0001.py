import socket
import ssl
import logging
from typing import Optional

class SecureNetworkMonitor:
    def __init__(self, host: str, port: int, timeout: int = 5):
        """
        Initialize the network monitor with secure defaults.
        
        Args:
            host: The hostname or IP address to check
            port: The port number to check
            timeout: Connection timeout in seconds
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self._setup_logging()

    def _setup_logging(self):
        """Set up secure logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='network_monitor.log',
            filemode='a'
        )

    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context."""
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        return context

    def check_server(self) -> Optional[bool]:
        """
        Check server availability securely.
        
        Returns:
            True if server is reachable, False if not, None if error occurs
        """
        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
                context = self._create_secure_context()
                with context.wrap_socket(sock, server_hostname=self.host) as secure_sock:
                    secure_sock.sendall(b"PING")
                    response = secure_sock.recv(1024)
                    return response == b"PONG"
        except (socket.timeout, ssl.SSLCertVerificationError, 
                ssl.SSLCertError, socket.error) as e:
            logging.error(f"Error checking server: {str(e)}")
            return None

if __name__ == "__main__":
    monitor = SecureNetworkMonitor("example.com", 443)
    result = monitor.check_server()
    if result is not None:
        print(f"Server {'is' if result else 'is not'} reachable")