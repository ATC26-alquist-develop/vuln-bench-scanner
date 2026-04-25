import ssl
import socket
import certifi
from typing import Optional
import logging
from urllib.parse import urlparse

def is_ssl_certificate_valid(url: str, timeout: int = 5) -> bool:
    """
    Securely check if a website's SSL certificate is valid.
    
    Args:
        url: The website URL to check
        timeout: Connection timeout in seconds
    
    Returns:
        bool: True if certificate is valid, False otherwise
    
    Raises:
        ValueError: If URL is invalid
        ssl.SSLCertVerificationError: If certificate verification fails
        socket.timeout: If connection times out
        socket.error: If connection fails
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid URL format")

        # Create secure SSL context
        context = ssl.create_default_context(cafile=certifi.where())
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Connect and verify certificate
        with socket.create_connection((parsed_url.hostname, 443), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=parsed_url.hostname) as secure_sock:
                logger.info(f"Successfully connected to {url}")
                return True

    except ssl.SSLCertVerificationError as e:
        logger.error(f"SSL certificate verification failed: {str(e)}")
        return False
    except socket.timeout:
        logger.error(f"Connection timed out for {url}")
        return False
    except socket.error as e:
        logger.error(f"Connection failed: {str(e)}")
        return False
    except ValueError as e:
        logger.error(f"Invalid URL: {str(e)}")
        return False