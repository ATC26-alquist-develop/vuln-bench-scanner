```python
import json
import hmac
import os
import secrets
from typing import Any, Dict
import ssl

class SecureProtocol:
    def __init__(self, secret_key: bytes):
        if len(secret_key) < 32:
            raise ValueError("Secret key must be at least 32 bytes long")
        self.secret_key = secret_key
        self._create_ssl_context()

    def _create_ssl_context(self) -> ssl.SSLContext:
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        return context

    def _generate_hmac(self, data: bytes) -> bytes:
        return hmac.new(self.secret_key, data, 'sha256').digest()

    def _verify_hmac(self, data: bytes, received_hmac: bytes) -> bool:
        expected_hmac = self._generate_hmac(data)
        return hmac.compare_digest(expected_hmac, received_hmac)

    def serialize(self, obj: Any) -> bytes:
        """Securely serialize an object to bytes."""
        json_data = json.dumps(obj, default=str).encode('utf-8')
        hmac_digest = self._generate_hmac(json_data)
        return hmac_digest + json_data

    def deserialize(self, data: bytes) -> Any:
        """Securely deserialize bytes to an object."""
        if len(data) < 32:  # Minimum HMAC length
            raise ValueError("Invalid data length")
        hmac_digest, json_data = data[:32], data[32:]
        if not self._verify_hmac(json_data, hmac_digest):
            raise ValueError("HMAC verification failed")
        return json.loads(json_data.decode('utf-8'))

    def send(self, data: Any, destination: str, port: int) -> None:
        """Send serialized data securely over SSL."""
        serialized = self.serialize(data)
        context = self._create_ssl_context()
        with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), 
                                server_hostname=destination) as s:
            s.connect((destination, port))
            s.sendall(serialized)

    def receive(self, source: str, port: int) -> Any:
        """Receive and deserialize data securely over SSL."""
        context = self._create_ssl_context()
        with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), 
                                server_hostname=source) as s:
            s.bind((source, port))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                received_data = conn.recv(4096)  # Adjust buffer size as needed
                return self.deserialize(received_data)
```