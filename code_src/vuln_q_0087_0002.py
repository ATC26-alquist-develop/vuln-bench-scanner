```python
import asyncio
import ssl
import logging
from typing import Tuple
from dataclasses import dataclass
from ssl import SSLContext, PROTOCOL_TLS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('secure_app.log')]
)
logger = logging.getLogger(__name__)

@dataclass
class ServerConfig:
    """Secure server configuration parameters"""
    host: str = '127.0.0.1'  # Localhost only
    port: int = 8443
    cert_path: str = None
    key_path: str = None

class SecureServer:
    def __init__(self, config: ServerConfig):
        self.config = config
        self._tasks: list[asyncio.Task] = []

    async def start(self):
        """Start the secure server with TLS"""
        try:
            # Create SSL context with strong defaults
            ssl_context = SSLContext(
                protocol=PROTOCOL_TLS,
                ciphers='ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256',
                options=ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
            )

            if self.config.cert_path and self.config.key_path:
                ssl_context.load_cert_chain(
                    certfile=self.config.cert_path,
                    keyfile=self.config.key_path,
                    password=None  # Store password securely, not in code
                )

            # Create TCP server with SSL
            server = await asyncio.start_server(
                self.handle_client, 
                self.config.host, 
                self.config.port, 
                ssl=ssl_context
            )

            addr = server.sockets[0].getsockname()
            logger.info(f'Server started on {addr}')

            async with server:
                await server.serve_forever()

        except Exception as e:
            logger.error(f'Server error: {str(e)}')
            raise

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handle client connections securely"""
        try:
            addr = writer.get_extra_info('peername')
            logger.info(f'New connection from {addr}')

            while True:
                data = await reader.read(1024)
                if not data:
                    break

                message = data.decode('utf-8').strip()
                logger.info(f'Received: {message}')

                # Echo back the received message
                response = f"Server received: {message}"
                writer.write(response.encode('utf-8'))
                await writer.drain()

        except Exception as e:
            logger.error(f'Error handling client: {str(e)}')
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(f'Connection closed for {addr}')

    async def stop(self):
        """Stop the server gracefully"""
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()
        logger.info('Server stopped')

async def main():
    """Main function to run the server"""
    try:
        config = ServerConfig(
            host='127.0.0.1',
            port=8443,
            cert_path='server.crt',
            key_path='server.key'
        )
        
        server = SecureServer(config)
        server_task = asyncio.create_task(server.start())

        # Keep the main coroutine running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info('Shutting down server...')
            await server.stop()
            await server_task
        finally:
            logger.info('Application shutdown complete')

if __name__ == '__main__':
    asyncio.run(main())
```


This implementation provides a secure client-server application with the following