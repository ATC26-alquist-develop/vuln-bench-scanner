import socket
import ssl
import logging
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureSocketPool:
    def __init__(self, max_connections: int = 10, timeout: int = 30):
        """Initialize secure socket pool with connection limits and timeouts"""
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

    def _create_secure_connection(self, host: str, port: int) -> Tuple[socket.socket, ssl.SSLSocket]:
        """Create secure connection with proper error handling"""
        try:
            sock = socket.create_connection((host, port), timeout=self.timeout)
            ssl_sock = self.ssl_context.wrap_socket(sock, server_hostname=host)
            return sock, ssl_sock
        except (socket.error, ssl.SSLError) as e:
            logging.error(f"Connection error: {e}")
            return None, None

    def connect(self, hosts: List[Tuple[str, int]]) -> List[Tuple[socket.socket, ssl.SSLSocket]]:
        """Establish secure connections to multiple hosts"""
        results = []
        for host, port in hosts:
            if not isinstance(host, str) or not isinstance(port, int):
                logging.warning(f"Invalid host or port: {host}:{port}")
                continue

            # Validate host
            if not host.isalnum():
                logging.warning(f"Invalid hostname: {host}")
                continue

            # Validate port
            if not 1 <= port <= 65535:
                logging.warning(f"Invalid port: {port}")
                continue

            future = self.pool.submit(self._create_secure_connection, host, port)
            sock, ssl_sock = future.result()
            if ssl_sock:
                results.append((sock, ssl_sock))
        return results

    def close(self):
        """Safely close all connections"""
        self.pool.shutdown(wait=True)
        for _, ssl_sock in self.connect([]):
            if ssl_sock:
                ssl_sock.close()

def main():
    # Example usage
    hosts = [
        ("example.com", 443),
        ("google.com", 443),
        ("python.org", 443)
    ]

    try:
        pool = SecureSocketPool()
        connections = pool.connect(hosts)
        
        for sock, ssl_sock in connections:
            if ssl_sock:
                print(f"Successfully connected to {ssl_sock.getpeername()}")
            else:
                print(f"Failed to connect to {sock.getpeername()}")
        
        # Keep pool open for reuse
        pool.close()
    except Exception as e:
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()