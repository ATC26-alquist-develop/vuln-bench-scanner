import asyncio
import ssl
import logging
from typing import Optional
from pathlib import Path

class SecureServer:
    def __init__(self, port: int = 8443, cert_path: Optional[str] = None, key_path: Optional[str] = None):
        """
        Initialize secure server with TLS configuration.
        
        Args:
            port: The port number to listen on (default 8443)
            cert_path: Path to SSL certificate file
            key_path: Path to SSL key file
        """
        self.port = port
        self.cert_path = cert_path
        self.key_path = key_path
        self._ssl_context: Optional[ssl.SSLContext] = None
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _load_ssl_context(self) -> None:
        """Load SSL context with strong security settings."""
        if not self.cert_path or not self.key_path:
            raise ValueError("Certificate and key paths must be provided")

        # Create context with strong security settings
        self._ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.CLIENT_AUTH,
            cafile=None  # We'll use system certs
        )
        
        # Load certificate and private key
        try:
            with open(self.cert_path, 'rb') as cert_file:
                self._ssl_context.load_cert_chain(
                    certfile=cert_file,
                    keyfile=self.key_path,
                    password=None  # Use PKCS7 or other secure auth method in production
                )
        except (IOError, ssl.SSLCertVerificationError) as e:
            logging.error(f"Failed to load SSL context: {e}")
            raise

    async def start(self):
        """Start the secure server."""
        try:
            # Load SSL context before starting
            self._load_ssl_context()

            # Create a secure server with IPv4 only
            server = await asyncio.start_server(
                self._handle_client, 
                '127.0.0.1',  # Listen only on localhost
                self.port,
                ssl=self._ssl_context
            )

            addr = server.sockets[0].getsockname()
            logging.info(f'Serving on {addr}')

            async with server:
                await server.serve_forever()

        except Exception as e:
            logging.error(f"Server error: {e}")
            raise

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle client connections securely."""
        try:
            addr = writer.get_extra_info('peername')
            logging.info(f"New connection from {addr}")

            # Handle client (implement your logic here)
            # Example: Echo back received data
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()

            # Clean up connection
            writer.close()
            await writer.wait_closed()
            logging.info(f"Connection closed for {addr}")

        except Exception as e:
            logging.error(f"Error handling client: {e}")

    def stop(self):
        """Stop the server."""
        if self._ssl_context:
            self._ssl_context = None
        logging.info("Server stopped")

# Usage example
if __name__ == "__main__":
    server = SecureServer(
        port=8443,
        cert_path="/path/to/fullchain.pem",
        key_path="/path/to/privkey.pem"
    )
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        server.stop()