import os
import ftplib
from typing import Optional
import logging
from pathlib import Path

class SecureFTPClient:
    def __init__(self, host: str, port: int = 21):
        """Initialize secure FTP client with proper error handling."""
        if not isinstance(host, str) or not host:
            raise ValueError("Invalid host parameter")
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError("Invalid port number")
            
        self.host = host
        self.port = port
        self._connection: Optional[ftplib.FTP] = None
        self._logger = logging.getLogger(__name__)

    def connect(self, username: str, password: str) -> bool:
        """Establish secure connection to FTP server."""
        try:
            # Validate inputs
            if not isinstance(username, str) or not username:
                raise ValueError("Invalid username")
            if not isinstance(password, str) or not password:
                raise ValueError("Invalid password")

            # Create secure connection
            self._connection = ftplib.FTP()
            self._connection.connect(
                self.host,
                port=self.port,
                timeout=10.0
            )
            
            # Set secure options
            self._connection.login(
                user=username,
                passwd=password
            )
            self._connection.prot_p()  # Enable password encryption
            
            # Set timeout for data connections
            self._connection.set_option(ftp_opt=203, value=10)
            
            self._logger.info("Secure FTP connection established")
            return True
            
        except (ftplib.all_errors, ValueError, OSError) as e:
            self._logger.error(f"Connection failed: {str(e)}")
            self._connection = None
            return False

    def close(self) -> None:
        """Safely close the FTP connection."""
        if self._connection:
            try:
                self._connection.quit()
                self._connection = None
            except Exception as e:
                self._logger.error(f"Error closing connection: {str(e)}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

def main():
    """Example usage with proper error handling."""
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        
        # Create secure FTP client
        with SecureFTPClient("ftp.example.com") as client:
            if client.connect("username", "password"):
                # Perform operations here
                pass
            else:
                print("Failed to connect")
                
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()