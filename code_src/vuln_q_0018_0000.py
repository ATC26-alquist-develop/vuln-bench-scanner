import socket
import ssl
import logging
from typing import Optional

def create_secure_connection(
    host: str,
    port: int,
    timeout: int = 10,
    max_size: int = 1024 * 1024  # 1MB limit
) -> Optional[socket.socket]:
    """
    Create a secure SSL/TLS connection to a remote server.
    
    Args:
        host: Server hostname or IP address
        port: Server port number
        timeout: Connection timeout in seconds
        max_size: Maximum allowed data size in bytes
    
    Returns:
        Secure socket object or None if connection fails
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Create a socket and wrap it with SSL
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                logger.info(f"Connected to {host}:{port}")
                
                # Set a maximum data size limit
                secure_sock.setsockopt(
                    ssl.SSLCLOEXEC, 
                    ssl.SSLCLOEXEC_MAXDATA, 
                    max_size
                )
                
                return secure_sock

    except (socket.timeout, socket.error) as e:
        logger.error(f"Connection failed: {str(e)}")
        return None
    except ssl.SSLCertVerificationError as e:
        logger.error(f"SSL certificate verification failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    HOST = "example.com"
    PORT = 443  # HTTPS port

    secure_socket = create_secure_connection(HOST, PORT)
    if secure_socket:
        try:
            # Example: Send a simple HTTP GET request
            request = f"GET / HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
            secure_socket.sendall(request.encode())
            
            # Receive response
            response = secure_socket.recv(4096)
            print(response.decode())
        finally:
            secure_socket.close()