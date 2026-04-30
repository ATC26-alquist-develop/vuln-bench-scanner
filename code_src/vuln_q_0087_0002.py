```python
import socket
import ssl
import os
from typing import Tuple
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureServer:
    def __init__(self, host: str, port: int):
        """Initialize secure server with TLS"""
        self.host = host
        self.port = port
        self.context = self._create_secure_context()
        
    def _create_secure_context(self) -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        return context

    @contextmanager
    def _secure_socket(self) -> ssl.SSLSocket:
        """Create secure socket with proper error handling"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(5)
            with self.context.wrap_socket(sock, server_side=True) as secure_sock:
                yield secure_sock
        except ssl.SSLCertVerificationError as e:
            logger.error(f"SSL certificate verification failed: {e}")
            raise
        except ssl.SSLError as e:
            logger.error(f"SSL error: {e}")
            raise
        finally:
            sock.close()

    def start(self):
        """Start secure server"""
        with self._secure_socket() as server:
            logger.info(f"Server listening on {self.host}:{self.port}")
            while True:
                try:
                    client, addr = server.accept()
                    logger.info(f"Accepted connection from {addr}")
                    self.handle_client(client)
                except ssl.SSLCertVerificationError:
                    logger.error("SSL certificate verification failed")
                    break
                except ssl.SSLError:
                    logger.error("SSL error occurred")
                    break
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")
                    break

    def handle_client(self, client: ssl.SSLSocket):
        """Handle client connection securely"""
        try:
            data = client.recv(1024)
            if not data:
                logger.warning("Client disconnected")
                return
            # Process data securely here
            response = b"Secure response"
            client.sendall(response)
        except ssl.SSLCertVerificationError:
            logger.error("SSL certificate verification failed")
        except ssl.SSLError:
            logger.error("SSL error occurred")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            client.close()

class SecureClient:
    def __init__(self, host: str, port: int):
        """Initialize secure client"""
        self.host = host
        self.port = port
        self.context = self._create_secure_context()

    def _create_secure_context(self) -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations("server.crt")
        return context

    def connect(self):
        """Establish secure connection"""
        with self._secure_socket() as sock:
            sock.connect((self.host, self.port))
            logger.info(f"Connected to {self.host}:{self.port}")
            return sock

    @contextmanager
    def _secure_socket(self):
        """Create secure socket with proper error handling"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.setsock