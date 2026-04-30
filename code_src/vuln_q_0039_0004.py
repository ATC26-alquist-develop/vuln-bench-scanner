```python
import socket
import ssl
import logging
from typing import Tuple, Optional

def create_secure_server(
    host: str = '127.0.0.1',  # Localhost by default
    port: int = 8443,
    cert_file: str = 'server.crt',
    key_file: str = 'server.key'
) -> Tuple[ssl.SSLSocket, ssl.SSLContext]:
    """
    Creates a secure SSL server that binds to localhost by default.
    Returns a tuple of (SSL socket, SSL context) for handling connections.
    """
    try:
        # Create SSL context with secure settings
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        
        # Create socket and wrap with SSL
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(5)
            with context.wrap_socket(sock, server_side=True) as secure_sock:
                return secure_sock, context
                
    except ssl.SSLError as e:
        logging.error(f"SSL error occurred: {e}")
        raise
    except socket.error as e:
        logging.error(f"Socket error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        raise
```