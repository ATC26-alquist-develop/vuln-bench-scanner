import socket
import ssl
import logging
from typing import Optional

def create_secure_server(host: str = '0.0.0.0', port: int = 443) -> Optional[ssl.SSLSocket]:
    """
    Creates a secure SSL server that listens on all available network interfaces.
    
    Args:
        host: The host address to bind to (default: '0.0.0.0' for all interfaces)
        port: The port number to listen on (default: 443)
    
    Returns:
        An SSL socket object if successful, None if an error occurs
    """
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set SO_REUSEADDR to allow the server to rebind to the same address
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to the specified host and port
        sock.bind((host, port))
        
        # Listen for incoming connections
        sock.listen(5)
        
        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        
        # Wrap the socket with SSL
        secure_sock = context.wrap_socket(sock, server_side=True)
        
        logging.info(f"Server started on {host}:{port}")
        
        return secure_sock
        
    except ssl.SSLCertVerificationError as e:
        logging.error(f"SSL certificate verification failed: {e}")
        return None
    except socket.error as e:
        logging.error(f"Socket error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def main():
    server_socket = create_secure_server()
    if server_socket:
        try:
            while True:
                client_socket, addr = server_socket.accept()
                logging.info(f"New connection from {addr}")
                # Handle the client connection here
                client_socket.close()
        except KeyboardInterrupt:
            logging.info("Server shutting down")
        finally:
            server_socket.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()