import socket
import ssl
import logging
from typing import Tuple
from ssl import SSLContext

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecureServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8443):
        self.host = host
        self.port = port
        self.socket = None
        self.context = self._create_ssl_context()
        
    def _create_ssl_context(self) -> SSLContext:
        """Create secure SSL context with strong security settings"""
        context = SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_verify_locations('path/to/ca_cert.pem')
        context.load_cert_chain(certfile='path/to/server.crt', keyfile='path/to/server.key')
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        return context

    def start(self) -> None:
        """Start the secure server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.socket.accept()
                secure_client = ssl_context.wrap_socket(
                    client_socket,
                    server_side=True,
                    cert_reqs=ssl.CERT_REQUIRED,
                    ssl_version=ssl.PROTOCOL_TLS_SERVER
                )
                logging.info(f"New connection from {address}")
                # Handle connection securely here
                
        except ssl.SSLError as e:
            logging.error(f"SSL error: {e}")
        except Exception as e:
            logging.error(f"Server error: {e}")
        finally:
            if self.socket:
                self.socket.close()

if __name__ == "__main__":
    server = SecureServer()
    server.start()