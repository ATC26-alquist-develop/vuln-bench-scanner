```python
import socket
import ssl
import logging
from typing import Optional
import time

class SecureServerChecker:
    def __init__(self, host: str, port: int, timeout: float = 5.0):
        """Initialize secure server checker with proper validation."""
        if not isinstance(host, str) or not host:
            raise ValueError("Invalid host")
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError("Invalid port")
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ValueError("Invalid timeout")
        
        self.host = host
        self.port = port
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def check_server(self) -> Optional[bool]:
        """Securely check server availability."""
        try:
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=self.host) as secure_sock:
                    self.logger.info(f"Successfully connected to {self.host}:{self.port}")
                    return True
        except (socket.timeout, ssl.SSLCertVerificationError, 
                socket.gaierror, socket.error) as e:
            self.logger.error(f"Failed to connect to {self.host}:{self.port}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error occurred: {str(e)}")
            return False
```