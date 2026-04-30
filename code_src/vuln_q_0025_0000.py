import ssl
import socket
import certifi
from typing import Optional
import logging
from urllib.parse import urlparse

def validate_ssl_certificate(url: str, timeout: int = 5) -> Optional[bool]:
    """
    Securely validate SSL certificate of a website.
    
    Args:
        url: Website URL to validate
        timeout: Connection timeout in seconds
        
    Returns:
        bool: True if certificate is valid, False if invalid, None if error
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Parse URL and validate format
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            logger.error("Invalid URL format")
            return None

        # Only allow HTTPS
        if parsed.scheme.lower() != 'https':
            logger.error("Only HTTPS URLs are allowed")
            return None

        # Create secure SSL context
        context = ssl.create_default_context(cafile=certifi.where())
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Connect with timeout
        with socket.create_connection((parsed.hostname, 443), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=parsed.hostname) as secure_sock:
                # Get certificate
                cert = secure_sock.getpeercert()
                
                # Basic certificate validation
                if not cert:
                    logger.error("No certificate found")
                    return False
                
                # Verify common name
                common_name = next((c[0] for c in cert if c[0] in ['subjectAltName', 'subjectCommonName']), None)
                if common_name and common_name not in parsed.netloc:
                    logger.error("Certificate common name doesn't match domain")
                    return False

                logger.info("SSL certificate is valid")
                return True

    except ssl.SSLCertVerificationError:
        logger.error("SSL certificate verification failed")
        return False
    except ssl.SSLCertHostnameKeyMismatch:
        logger.error("Certificate hostname doesn't match")
        return False
    except ssl.SSLCertExpired:
        logger.error("Certificate has expired")
        return False
    except ssl.SSLCertNotFound:
        logger.error("Certificate not found")
        return False
    except socket.timeout:
        logger.error("Connection timed out")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None