import json
import ssl
import socket
from typing import Any
from cryptography.fernet import Fernet

class SecureProtocol:
    def __init__(self, host: str, port: int, key: bytes):
        """Initialize secure protocol with TLS"""
        self.host = host
        self.port = port
        self.key = key
        self.fernet = Fernet(key)
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    def serialize(self, obj: Any) -> bytes:
        """Securely serialize object"""
        json_data = json.dumps(obj).encode('utf-8')
        return self.fernet.encrypt(json_data)

    def deserialize(self, data: bytes) -> Any:
        """Securely deserialize object"""
        decrypted_data = self.fernet.decrypt(data)
        return json.loads(decrypted_data.decode('utf-8'))

    def send(self, obj: Any) -> None:
        """Send serialized object securely"""
        serialized = self.serialize(obj)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            with self.context.wrap_socket(s, server_side=True) as secure_socket:
                secure_socket.connect((self.host, self.port))
                secure_socket.sendall(serialized)

    def receive(self) -> Any:
        """Receive and deserialize object securely"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            with self.context.wrap_socket(s, server_hostname=self.host) as secure_socket:
                secure_socket.connect((self.host, self.port))
                data = secure_socket.recv(4096)
                return self.deserialize(data)

# Usage example
if __name__ == "__main__":
    # Generate a secure key (in production, use a proper key management system)
    key = Fernet.generate_key()
    
    # Initialize protocol
    protocol = SecureProtocol("localhost", 12345, key)
    
    # Send data
    protocol.send({"message": "Hello, secure world!"})
    
    # Receive data
    received_data = protocol.receive()
    print(received_data)