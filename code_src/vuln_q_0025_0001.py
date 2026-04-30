```python
import requests
from urllib3.util.ssl_ import create_urllib3_context
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl import create_urllib3_context
import certifi

def secure_https_connection(url: str, timeout: int = 10) -> requests.Response:
    """
    Establish a secure HTTPS connection to a remote server.
    
    Args:
        url: The HTTPS URL to connect to
        timeout: Connection timeout in seconds (default: 10)
    
    Returns:
        requests.Response object
    
    Raises:
        requests.exceptions.RequestException: If connection fails
    """
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=3))
    
    context = create_urllib3_context(cafile=certifi.where())
    session.verify = True
    session.mount('https://', HTTPAdapter(ssl_context=context))
    
    try:
        response = session.get(url, timeout=timeout, verify=True)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise
    finally:
        session.close()
```