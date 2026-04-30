import socket
import ssl
import logging
from typing import Optional
from pathlib import Path

def create_secure_socket_connection(
    target_host: str,
    target_port: int,
    data: bytes,
    timeout: float = 5.0
) -> Optional[tuple[socket.socket, ssl.SSLSocket]]:
    """
    Create a secure socket connection to send data to a target host and port.
    
    Args:
        target_host: Target IP address or hostname
        target_port: Target port number
        data: Data to send (bytes)
        timeout: Connection timeout in seconds
        
    Returns:
        Tuple of (socket.socket, ssl.SSLSocket) if successful, None otherwise
    """
    # Input validation
    if not isinstance(target_host, str) or not target_host:
        raise ValueError("Invalid target host")
    
    if not isinstance(target_port, int) or target_port < 1 or target_port > 65535:
        raise ValueError("Invalid target port")
        
    if not isinstance(data, bytes):
        raise ValueError("Data must be bytes")
        
    if not isinstance(timeout, (int, float)) or timeout <= 0:
        raise ValueError("Invalid timeout value")

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Create a TCP/IP socket with timeout
        with socket.create_connection((target_host, target_port), timeout=timeout) as sock:
            # Create SSL context with strong defaults
            context = ssl.create_default_context()
            
            # Wrap the socket with SSL/TLS
            with context.wrap_socket(
                sock,
                server_hostname=target_host  # Enable hostname verification
            ) as secure_sock:
                logging.info(f"Connected to {target_host}:{target_port}")
                
                # Send data
                secure_sock.sendall(data)
                
                # Receive response (optional, remove if not needed)
                response = secure_sock.recv(4096)
                
                logging.info(f"Received response: {response.decode('utf-8', errors='ignore')}")
                
                return (sock, secure_sock)

    except (socket.timeout, socket.error, ssl.SSLCertVerificationError) as e:
        logging.error(f"Connection failed: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None