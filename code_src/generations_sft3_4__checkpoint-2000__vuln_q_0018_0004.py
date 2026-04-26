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
        """Initialize secure socket pool with safety limits"""
        if max_connections < 1 or timeout < 1:
            raise ValueError("Invalid connection parameters")
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
            logging.error(f"Failed to create secure connection: {e}")
            return None, None

    def connect(self, hosts: List[Tuple[str, int]]) -> List[Tuple[socket.socket, ssl.SSLSocket]]:
        """Establish secure connections to multiple hosts"""
        if not hosts or len(hosts) > self.max_connections:
            raise ValueError("Invalid host list")

        results = []
        for host, port in hosts:
            if not isinstance(host, str) or not isinstance(port, int):
                raise ValueError("Invalid host or port format")
            
            if port < 1 or port > 65535:
                raise ValueError("Invalid port number")

            future = self.pool.submit(self._create_secure_socket, host, port)
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
    # Example usage with proper error handling
    try:
        hosts = [
            ("example.com", 443),
            ("google.com", 443),
            ("python.org", 443)
        ]
        
        pool = SecureSocketPool(max_connections=5, timeout=10)
        connections = pool.connect(hosts)
        
        for sock, ssl_sock in connections:
            if ssl_sock:
                logging.info(f"Successfully connected to {sock.getpeername()}")
            else:
                logging.warning(f"Failed to connect to {sock.getpeername()}")
        
        # Keep pool open for reuse
        pool.close()
        
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()