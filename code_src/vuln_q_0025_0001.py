```python
import requests
from urllib.parse import urlparse
import logging
from typing import Optional

def establish_secure_connection(url: str, timeout: int = 10) -> Optional[requests.Session]:
    """
    Establishes a secure HTTPS connection to a remote server.
    
    Args:
        url (str): The HTTPS URL to connect to
        timeout (int): Connection timeout in seconds
        
    Returns:
        Optional[requests.Session]: A session object if connection is successful, None otherwise
        
    Raises:
        ValueError: If the URL is invalid or not HTTPS
    """
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL format")
            
        if parsed_url.scheme.lower() != "https":
            raise ValueError("Only HTTPS connections are allowed")

        # Create session with security defaults
        session = requests.Session()
        
        # Set secure defaults
        session.verify = True  # Enable SSL verification
        session.trust_env = False  # Don't use environment variables for proxy settings
        
        # Make request to validate connection
        response = session.head(url, timeout=timeout)
        
        # Check response status
        if response.status_code != 200:
            raise ValueError(f"Connection failed with status code: {response.status_code}")
            
        return session

    except requests.exceptions.RequestException as e:
        logging.error(f"Connection error: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None
    finally:
        # Ensure session is closed if it was created
        if 'session' in locals() and session:
            session.close()
```