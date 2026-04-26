import socket
import ssl
import threading
from typing import Tuple

class SecureServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 8443):
        self.host = host
        self.port = port
        self.context = self._create_ssl_context()
        self.socket = None

    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create a secure SSL context with strong security settings."""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        return context

    def start(self):
        """Start the secure server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            try:
                client_socket, addr = self.socket.accept()
                print(f"New connection from {addr}")
                self._handle_client(client_socket, addr)
            except ssl.SSLError as e:
                print(f"SSL error: {e}")
            except Exception as e:
                print(f"Error: {e}")

    def _handle_client(self, client_socket: ssl.SSLSocket, addr: Tuple[str, int]):
        """Handle client connection securely."""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process data securely here
                response = self._process_data(data)
                client_socket.sendall(response)
        except ssl.SSLError as e:
            print(f"SSL error with {addr}: {e}")
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            client_socket.close()

    def _process_data(self, data: bytes) -> bytes:
        """Process received data securely."""
        # Implement secure data processing logic here
        return b"Processed data"

    def stop(self):
        """Safely stop the server."""
        if self.socket:
            self.socket.close()
        print("Server stopped")

if __name__ == "__main__":
    server = SecureServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server stopping...")
    finally:
        server.stop()