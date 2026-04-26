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
        """Initialize secure socket pool with safety limits"""
        if max_connections < 1 or max_connections > 100:
            raise ValueError("Max connections must be between 1 and 100")
        if timeout < 5 or timeout > 60:
            raise ValueError("Timeout must be between 5 and 60 seconds")
            
        self.max_connections = max_connections
        self.timeout = timeout
        self.pool = ThreadPoolExecutor(max_workers=max_connections)
        self.ssl_context = self._create_secure_context()

    def _create_secure_context(self) -> ssl.SSLContext:
        """Create secure SSL context with strong settings"""
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_default_certs()
        return context

    def _create_secure_socket(self, host: str, port: int) -> Tuple[socket.socket, ssl.SSLSocket]:
        """Create secure socket connection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # Wrap socket with SSL
            ssl_sock = self.ssl_context.wrap_socket(sock, server_hostname=host)
            
            logger.info(f"Establishing connection to {host}:{port}")
            ssl_sock.connect((host, port))
            return sock, ssl_sock
        except (socket.timeout, socket.error) as e:
            logger.error(f"Connection failed: {str(e)}")
            raise

    def connect(self, hosts: List[Tuple[str, int]]) -> List[ssl.SSLSocket]:
        """Establish secure connections to multiple hosts"""
        if not hosts or len(hosts) > self.max_connections:
            raise ValueError("Invalid host list")

        # Validate host format
        for host, port in hosts:
            if not isinstance(host, str) or not isinstance(port, int):
                raise ValueError("Invalid host or port format")
            if port < 1 or port > 65535:
                raise ValueError("Invalid port number")

        # Create connections using thread pool
        return list(self.pool.map(
            lambda h: self._create_secure_socket(h[0], h[1]),
            hosts
        ))

    def __del__(self):
        """Ensure proper cleanup"""
        self.pool.shutdown(wait=True)