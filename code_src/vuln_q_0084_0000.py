import socket
import ssl
import logging
from typing import Optional

class SecureSocket:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context: Optional[ssl.SSLContext] = None
        self.socket: Optional[socket.socket] = None

    def __enter__(self):
        self._create_context()
        self._create_socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()

    def _create_context(self) -> None:
        """Create a secure SSL context."""
        try:
            self.context = ssl.create_default_context()
            self.context.check_hostname = True
            self.context.verify_mode = ssl.CERT_REQUIRED
        except ssl.SSLCertVerificationError as e:
            logging.error(f"SSL certificate verification failed: {e}")
            raise
        except Exception as e:
            logging.error(f"Failed to create SSL context: {e}")
            raise

    def _create_socket(self) -> None:
        """Create a secure socket."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(30)  # Set timeout to prevent hanging
            self.socket.connect((self.host, self.port))
            self.socket = self.context.wrap_socket(self.socket, server_hostname=self.host)
        except socket.error as e:
            logging.error(f"Socket connection failed: {e}")
            raise
        except ssl.SSLCertVerificationError as e:
            logging.error(f"SSL certificate verification failed: {e}")
            raise
        except Exception as e:
            logging.error(f"Failed to create secure socket: {e}")
            raise

    def _close(self) -> None:
        """Close the socket connection."""
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                logging.error(f"Failed to close socket: {e}")
            finally:
                self.socket = None

def main():
    host = "example.com"
    port = 443  # HTTPS port

    try:
        with SecureSocket(host, port) as secure_socket:
            # Perform secure operations here
            print("Secure connection established")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()