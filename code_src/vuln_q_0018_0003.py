import socket
import ssl
import logging
from typing import Optional, Tuple

def create_secure_socket_connection(
    host: str,
    port: int,
    data: Optional[bytes] = None,
    timeout: int = 30
) -> Tuple[bool, Optional[bytes]]:
    """
    Create a secure socket connection to send data to a specific IP address and port.
    
    Args:
        host: Target IP address
        port: Target port number
        data: Optional data to send (in bytes)
        timeout: Connection timeout in seconds
    
    Returns:
        Tuple of (success: bool, received_data: Optional[bytes])
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
                logger.info(f"Successfully connected to {host}:{port}")
                
                if data:
                    # Send data securely
                    secure_sock.sendall(data)
                    logger.info(f"Sent {len(data)} bytes of data")
                
                # Receive response (if any)
                received_data = secure_sock.recv(4096)
                logger.info(f"Received {len(received_data)} bytes of response")
                
                return True, received_data

    except ssl.SSLCertVerificationError as e:
        logger.error(f"SSL certificate verification failed: {str(e)}")
        return False, None
    except socket.timeout:
        logger.error(f"Connection timed out after {timeout} seconds")
        return False, None
    except socket.error as e:
        logger.error(f"Socket error occurred: {str(e)}")
        return False, None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False, None