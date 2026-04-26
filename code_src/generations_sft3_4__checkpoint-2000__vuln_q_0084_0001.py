import socket
import ssl
import secrets
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureSocket:
    def __init__(self, host: str, port: int, cert_path: str, key_path: str):
        """Initialize secure socket with TLS"""
        self.host = host
        self.port = port
        self.cert_path = cert_path
        self.key_path = key_path
        self.context = self._create_context()
        
    def _create_context(self) -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.cert_path, keyfile=self.key_path)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        return context

    def start_server(self) -> Tuple[socket.socket, ssl.SSLSocket]:
        """Start secure server"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((self.host, self.port))
                sock.listen(5)
                logging.info(f"Server listening on {self.host}:{self.port}")
                
                # Accept connection
                with self.context.wrap_socket(sock, server_side=True) as secure_sock:
                    conn, addr = secure_sock.accept()
                    logging.info(f"Connection from {addr}")
                    return conn, secure_sock
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
            raise

    def start_client(self, host: str, port: int) -> Tuple[ssl.SSLSocket, socket.socket]:
        """Start secure client"""
        try:
            with socket.create_connection((host, port)) as sock:
                with self.context.wrap_socket(sock, server_hostname=host) as secure_sock:
                    return secure_sock, sock
        except Exception as e:
            logging.error(f"Client error: {str(e)}")
            raise

def main():
    # Example usage
    try:
        # Server setup
        server = SecureSocket('localhost', 8443, 'server.crt', 'server.key')
        conn, secure_conn = server.start_server()
        
        # Send data
        message = "Hello, secure world!"
        secure_conn.sendall(message.encode())
        
        # Receive data
        data = conn.recv(1024)
        print(f"Received: {data.decode()}")
        
    except Exception as e:
        logging.error(f"Main error: {str(e)}")

if __name__ == "__main__":
    main()