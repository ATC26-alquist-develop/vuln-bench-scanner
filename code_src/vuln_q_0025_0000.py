import ssl
import socket
import logging
from typing import Optional
from urllib.parse import urlparse

def validate_ssl_certificate(url: str, timeout: int = 5) -> Optional[bool]:
    """
    Validates the SSL certificate of a website.
    
    Args:
        url: The website URL to validate
        timeout: Connection timeout in seconds
        
    Returns:
        True if certificate is valid, False if invalid, None if error
    """
    # Input validation
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL format")
        if parsed.scheme.lower() != "https":
            raise ValueError("Only HTTPS URLs are supported")
    except Exception as e:
        logging.error(f"URL validation error: {str(e)}")
        return None

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        # Get hostname and port from URL
        hostname = parsed.netloc
        port = parsed.port or 443  # Default to 443 if no port specified

        # Create context with high security settings
        context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH,
            cafile=None,  # Use system's root certificates
            check_hostname=True,
            minimum_version=ssl.TLSVersion.TLSv1_2
        )

        # Disable insecure cipher suites
        context.set_ciphers('HIGH:!aNULL:!MD5:!RC4')

        # Create socket and wrap with SSL context
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Get certificate information
                cert = ssock.getpeercert(binary_form=True)
                
                # Basic certificate validation
                if not cert:
                    logging.error("No certificate received")
                    return False

                # Verify certificate is not expired
                if ssl.cert_time(ssock.getpeercert(binary_form=True)):
                    logging.info(f"Certificate is valid for {ssl.cert_time(ssock.getpeercert(binary_form=True))}")
                    return True

                logging.error("Certificate is invalid or expired")
                return False

    except (socket.timeout, socket.gaierror, ssl.SSLCertVerificationError) as e:
        logging.error(f"Connection error: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None