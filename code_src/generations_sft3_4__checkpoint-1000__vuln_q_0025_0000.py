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
        
        # Create socket
        with socket.create_connection((hostname, 443), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                # Verify certificate
                if secure_sock.version() != ssl.PROTOCOL_TLS:
                    logger.error("Unsupported TLS version")
                    return None
                    
                # Check certificate validity
                cert = secure_sock.getpeercert()
                if not cert:
                    logger.error("No certificate found")
                    return None
                    
                # Verify basic certificate validity
                if not cert['notAfter'] or not cert['notBefore']:
                    logger.error("Invalid certificate dates")
                    return None
                    
                # Verify certificate is not expired
                if ssl.cert_time_to_seconds(cert['notAfter']) < ssl.cert_time_to_seconds(ssl.CERT_TIME_NOW):
                    logger.error("Certificate has expired")
                    return None
                    
                logger.info("SSL certificate is valid")
                return True
                
    except (socket.timeout, ssl.SSLError, socket.error) as e:
        logger.error(f"Error checking SSL certificate: {str(e)}")
        return None