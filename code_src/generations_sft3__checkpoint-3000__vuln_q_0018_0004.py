import socket
import ssl
import logging
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocketPool:
    def __init__(self, max_connections: int = 10, timeout: int = 30):
        """
        Initialize secure socket pool with connection limits and timeouts
        
        Args:
            max_connections: Maximum number of concurrent connections
            timeout: Connection timeout in seconds
        """
        self.max_connections = max_connections
        self.timeout = timeout
        self.pool = ThreadPoolExecutor(max_workers=max_connections)
        self.ssl_context = self._create_ssl_context()

    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_default_certs()
        return context

    def _create_secure_socket(self, host: str, port: int) -> Tuple[socket.socket, ssl.SSLSocket]:
        """Create secure socket connection"""
        try:
            sock = socket.create_connection((host, port), timeout=self.timeout)
            ssl_sock = self.ssl_context.wrap_socket(sock, server_hostname=host)
            return sock, ssl_sock
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Failed to create secure connection: {e}")
            return None, None

    def connect(self, hosts: List[Tuple[str, int]]) -> List[Tuple[socket.socket, ssl.SSLSocket]]:
        """Establish secure connections to multiple hosts"""
        if not hosts or len(hosts) > self.max_connections:
            logger.error("Invalid host list")
            return []

        connections = []
        for host, port in hosts:
            if not isinstance(host, str) or not isinstance(port, int):
                logger.error(f"Invalid host or port: {host}:{port}")
                continue

            if port < 1 or port > 65535:
                logger.error(f"Invalid port: {port}")
                continue

            future = self.pool.submit(self._create_secure_socket, host, port)
            sock, ssl_sock = future.result()
            if ssl_sock:
                connections.append((sock, ssl_sock))

        return connections

    def close(self):
        """Safely close all connections"""
        self.pool.shutdown(wait=True)
        for sock, ssl_sock in self.pool._done:
            if ssl_sock:
                ssl_sock.close()
        self.ssl_context = None

def main():
    # Example usage
    hosts = [
        ("example.com", 443),
        ("google.com", 443),
        ("python.org", 443)
    ]

    pool = SecureSocketPool(max_connections=5, timeout=10)
    try:
        connections = pool.connect(hosts)
        for sock, ssl_sock in connections:
            if ssl_sock:
                logger.info(f"Successfully connected to {ssl_sock.getpeername()}")
    except Exception as e:
        logger.error(f"Error in connection pool: {e}")
    finally:
        pool.close()

if __name__ == "__main__":
    main()