import ssl
import socket
from typing import Tuple
import logging
from urllib.parse import urlparse

def check_ssl_certificate(hostname: str, port: int = 443) -> Tuple[bool, str]:
    """
    Securely check SSL certificate validity for a given hostname.
    
    Args:
        hostname: Target hostname to check
        port: Target port (default 443)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Input validation
    if not isinstance(hostname, str) or not isinstance(port, int):
        return False, "Invalid input types"
        
    if port < 1 or port > 65535:
        return False, "Invalid port number"
        
    try:
        # Create secure SSL context
        context = ssl.create_default_context()
        
        # Disable older insecure protocols
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        
        # Create socket and wrap with SSL
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                # Verify certificate
                cert = secure_sock.getpeercert()
                if not cert:
                    return False, "No certificate received"
                    
                # Check certificate validity
                if not ssl.check_hostname:
                    logger.warning("Hostname verification is disabled")
                    ssl.check_hostname = True
                    
                try:
                    # Verify certificate is not expired
                    secure_sock.verify_certificate()
                    return True, "Certificate is valid"
                    
                except ssl.CertificateError as e:
                    return False, f"Certificate error: {str(e)}"
                    
    except (socket.timeout, ssl.SSLError, socket.error) as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False, "Unexpected error occurred"