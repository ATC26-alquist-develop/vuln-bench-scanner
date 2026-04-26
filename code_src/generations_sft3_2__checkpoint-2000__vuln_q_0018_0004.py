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

    def _create_secure_socket(self, host: str, port: int) -> Tuple[socket.socket, ssl.SSLSocket]:
        """Create secure socket connection"""
        try:
            sock = socket.create_connection((host, port), timeout=self.timeout)
            ssl_sock = self.ssl_context.wrap_socket(sock, server_hostname=host)
            return sock, ssl_sock
        except (socket.error, ssl.SSLError) as e:
            logging.error(f"Failed to create secure connection to {host}:{port}: {str(e)}")
            return None, None

    def connect(self, hosts: List[Tuple[str, int]]) -> List[Tuple[ssl.SSLSocket, ssl.SSLSocket]]:
        """Establish secure connections to multiple hosts"""
        if not hosts or len(hosts) > self.max_connections:
            logging.error("Invalid host list")
            return []

        results = []
        for host, port in hosts:
            if not isinstance(host, str) or not isinstance(port, int):
                logging.error(f"Invalid host or port format: {host}:{port}")
                continue

            secure_sock = None
            try:
                secure_sock, _ = self._create_secure_socket(host, port)
                if secure_sock:
                    results.append((secure_sock, secure_sock))
            except Exception as e:
                logging.error(f"Connection error for {host}:{port}: {str(e)}")
            finally:
                if secure_sock:
                    secure_sock.close()

        return results

    def close(self):
        """Safely close all connections"""
        self.pool.shutdown(wait=True)
        for conn in self.pool._pool:
            conn.close()

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
        
        if connections:
            for conn in connections:
                print(f"Successfully connected to {conn[0].getpeername()}")
        else:
            print("No connections established")
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
    finally:
        pool.close()

if __name__ == "__main__":
    main()