```python
import json
import ssl
import logging
from typing import Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecureProtocol:
    def __init__(self, encryption_key: bytes):
        """Initialize with a secure encryption key."""
        if not isinstance(encryption_key, bytes) or len(encryption_key) < 32:
            raise ValueError("Encryption key must be bytes with at least 32 bytes")
        
        # Use PBKDF2 to derive a secure key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'secure_salt',  # In practice, use a unique salt per session
            iterations=100000,
            backend=default_backend()
        )
        self.fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(encryption_key))
        
    def serialize(self, obj: Any) -> bytes:
        """Securely serialize an object."""
        try:
            # Convert object to JSON
            json_data = json.dumps(obj, default=str)
            
            # Encrypt the JSON data
            encrypted_data = self.fernet.encrypt(json_data.encode('utf-8'))
            
            return encrypted_data
        except (TypeError, ValueError, json.JSONDecodeError) as e:
            logger.error(f"Serialization error: {str(e)}")
            raise

    def deserialize(self, data: bytes) -> Any:
        """Securely deserialize an object."""
        try:
            # Decrypt the data
            decrypted_data = self.fernet.decrypt(data)
            
            # Parse JSON
            obj = json.loads(decrypted_data.decode('utf-8'))
            
            return obj
        except (TypeError, ValueError, json.JSONDecodeError, ssl.SSLCertVerificationError) as e:
            logger.error(f"Deserialization error: {str(e)}")
            raise

    def send(self, data: Any, host: str, port: int) -> None:
        """Send data securely over TLS."""
        if not isinstance(host, str) or not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError("Invalid host or port")

        try:
            context = ssl.create_default_context()
            with socket.create_connection((host, port)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                    logger.info(f"Connected to {host}:{port}")
                    encrypted_data = self.serialize(data)
                    secure_sock.sendall(encrypted_data)
        except (socket.error, ssl.SSLCertVerificationError) as e:
            logger.error(f"Connection error: {str(e)}")
            raise

    def receive(self) -> Any:
        """Receive data securely and deserialize."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5.0)  # Set a reasonable timeout
                sock.bind(('localhost', 0))  # Use localhost and a random port
                port = sock.getsockname()[1]
                sock.listen(1)
                logger.info(f"Listening on port {port}")
                
                with context.wrap_socket(sock, server_side=True) as secure_sock:
                    try:
                        conn, addr = secure_sock.accept()
                        logger.info(f"Connection from {addr}")
                        encrypted_data = conn.recv(4096)
                        conn.close()
                        
                        #