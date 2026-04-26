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
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        
        # Connect to the target
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                # Verify certificate
                cert = secure_sock.getpeercert()
                
                if not cert:
                    return False, "No certificate received"
                
                # Check certificate validity
                if not ssl.check_hostname:
                    logger.warning("Hostname verification is disabled")
                    ssl._ssl._context.set_verify(ssl.CERT_REQUIRED, ssl.CERT_IGNORING_UNSAFE_RANGES)
                
                if not ssl.verify_certificate(secure_sock.getpeercert(), secure_sock.getpeercert(chain=True)):
                    return False, "Certificate verification failed"
                
                return True, "Certificate is valid"
                
    except ssl.SSLError as e:
        logger.error(f"SSL error occurred: {str(e)}")
        return False, "SSL error occurred"
    except socket.gaierror:
        logger.error("DNS lookup failed")
        return False, "DNS lookup failed"
    except socket.error as e:
        logger.error(f"Socket error occurred: {str(e)}")
        return False, "Connection error occurred"
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return False, "Unexpected error occurred"

if __name__ == "__main__":
    # Example usage
    result, message = check_ssl_certificate("example.com")
    print(f"Certificate valid: {result}")
    print(f"Message: {message}")