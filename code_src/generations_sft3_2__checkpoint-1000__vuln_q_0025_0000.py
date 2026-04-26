import ssl
import socket
import logging
from typing import Optional

def check_ssl_certificate(hostname: str, timeout: float = 5.0) -> Optional[bool]:
    """
    Securely check if a website's SSL certificate is valid.
    
    Args:
        hostname: The domain name to check
        timeout: Connection timeout in seconds
    
    Returns:
        bool: True if certificate is valid, False if invalid, None if error
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Validate input
        if not isinstance(hostname, str) or not hostname:
            logger.error("Invalid hostname format")
            return None
            
        # Create secure SSL context
        context = ssl.create_default_context()
        
        # Set timeout
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Connect to the host
        with socket.create_connection((hostname, 443), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                # Verify certificate
                if secure_sock.version() != 'TLSv1.2':
                    logger.warning("Insecure TLS version detected")
                    return False
                    
                return True
                
    except (ssl.SSLError, socket.error) as e:
        logger.error(f"SSL certificate check failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None