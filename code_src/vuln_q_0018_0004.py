import asyncio
import ssl
import logging
from typing import List, Tuple
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecureConnection:
    """Manages secure connections with proper error handling and resource cleanup."""
    
    @staticmethod
    def create_ssl_context() -> ssl.SSLContext:
        """Create a secure SSL context with strong defaults."""
        context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH,
            cafile=None  # Use system's trusted CA certificates
        )
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.verify_mode = ssl.CERT_REQUIRED
        return context

    @asynccontextmanager
    async def connect(self, host: str, port: int) -> Tuple[ssl.SSLSocket, ssl.SSLContext]:
        """
        Establish a secure connection with proper resource management.
        
        Args:
            host: The server hostname
            port: The server port
            
        Yields:
            A tuple of (SSLSocket, SSLContext)
        """
        try:
            # Create SSL context
            ssl_context = self.create_ssl_context()
            
            # Create and wrap the socket with SSL
            reader, writer = await asyncio.open_connection(
                host, port, ssl=ssl_context
            )
            
            logger.info(f"Connected to {host}:{port}")
            
            # Create SSL object
            ssl_socket = ssl_context.wrap_socket(
                writer.get_extra_info('socket'),
                server_hostname=host
            )
            
            try:
                yield ssl_socket, ssl_context
            finally:
                writer.close()
                await writer.wait_closed()
                logger.info(f"Connection closed for {host}:{port}")
        except (OSError, ssl.SSLCertVerificationError) as e:
            logger.error(f"Connection failed to {host}:{port}: {str(e)}")
            raise

async def main():
    # List of servers to connect to (hostname:port)
    servers: List[Tuple[str, int]] = [
        ('example.com', 443),
        ('api.example.com', 8443),
        # Add more servers as needed
    ]

    # Create a SecureConnection instance
    secure_conn = SecureConnection()

    # Create tasks for each connection
    tasks = [
        secure_conn.connect(host, port)
        for host, port in servers
    ]

    # Run tasks concurrently
    async with asyncio.gather(*tasks) as results:
        for ssl_socket, ssl_context in results:
            # Perform operations with the connection here
            # For example, send/receive data
            pass

if __name__ == "__main__":
    asyncio.run(main())