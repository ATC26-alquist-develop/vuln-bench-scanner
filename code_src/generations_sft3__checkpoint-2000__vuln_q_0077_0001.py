```python
import json
import base64
import hmac
import hashlib
import os
from typing import Any, Dict
from dataclasses import dataclass
from enum import Enum, auto

class MessageType(Enum):
    """Secure message types"""
    REQUEST = auto()
    RESPONSE = auto()

@dataclass
class SecureMessage:
    """Secure message container with integrity check"""
    message_type: MessageType
    payload: str
    signature: str

class SecureProtocol:
    """Secure network protocol implementation"""
    
    def __init__(self, secret_key: bytes):
        """Initialize with a secret key"""
        if not isinstance(secret_key, bytes) or len(secret_key) < 32:
            raise ValueError("Secret key must be bytes with minimum length of 32")
        self.secret_key = secret_key

    def serialize(self, obj: Any) -> str:
        """Securely serialize object to JSON"""
        try:
            # Use JSON for serialization
            json_data = json.dumps(obj, sort_keys=True)
            # Encode to base64 for safe transport
            encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
            return encoded_data
        except (TypeError, ValueError) as e:
            raise ValueError(f"Serialization failed: {str(e)}")

    def deserialize(self, data: str) -> Any:
        """Securely deserialize object from JSON"""
        try:
            # Decode and parse JSON
            json_data = base64.b64decode(data).decode('utf-8')
            return json.loads(json_data)
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Deserialization failed: {str(e)}")

    def sign(self, data: str) -> str:
        """Create HMAC signature for data"""
        try:
            # Create HMAC signature
            signature = hmac.new(
                key=self.secret_key,
                msg=data.encode('utf-8'),
                digestmod=hashlib.sha256
            ).hexdigest()
            return signature
        except Exception as e:
            raise ValueError(f"Signature creation failed: {str(e)}")

    def encrypt(self, data: str) -> str:
        """Placeholder for encryption (not implemented in this example)"""
        raise NotImplementedError("Encryption not implemented in this example")

    def decrypt(self, data: str) -> str:
        """Placeholder for decryption (not implemented in this example)"""
        raise NotImplementedError("Decryption not implemented in this example")

    def create_message(self, obj: Any) -> SecureMessage:
        """Create a secure message"""
        try:
            serialized = self.serialize(obj)
            signature = self.sign(serialized)
            return SecureMessage(
                message_type=MessageType.REQUEST,
                payload=serialized,
                signature=signature
            )
        except ValueError as e:
            raise ValueError(f"Message creation failed: {str(e)}")

    def verify_and_process(self, message: SecureMessage) -> Any:
        """Verify and process a secure message"""
        try:
            # Verify signature
            if not hmac.compare_digest(
                message.signature.encode('utf-8'),
                self.sign(message.payload).encode('utf-8')
            ):
                raise ValueError("Invalid signature")

            # Deserialize and process
            obj = self.deserialize(message.payload)
            return obj
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Message processing failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Generate a secure random key
    secret_key = os.urandom(32)
    
    # Initialize protocol
    protocol = SecureProtocol(secret_key)
    
    # Example object
    data = {"key": "value", "number": 42}
    
    # Create message
    message = protocol.create