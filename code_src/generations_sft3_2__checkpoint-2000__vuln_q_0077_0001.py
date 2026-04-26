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
        """Securely deserialize JSON data"""
        try:
            # Decode and parse JSON
            json_data = base64.b64decode(data).decode('utf-8')
            return json.loads(json_data)
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Deserialization failed: {str(e)}")

    def generate_signature(self, data: str) -> str:
        """Generate HMAC signature for data"""
        try:
            # Use SHA256 for signature
            signature = hmac.new(
                key=self.secret_key,
                msg=data.encode('utf-8'),
                digestmod=hashlib.sha256
            ).hexdigest()
            return signature
        except Exception as e:
            raise ValueError(f"Signature generation failed: {str(e)}")

    def create_message(self, obj: Any) -> SecureMessage:
        """Create a secure message with signature"""
        try:
            serialized = self.serialize(obj)
            signature = self.generate_signature(serialized)
            return SecureMessage(
                message_type=MessageType.REQUEST,
                payload=serialized,
                signature=signature
            )
        except ValueError as e:
            raise ValueError(f"Message creation failed: {str(e)}")

    def verify_message(self, message: SecureMessage) -> bool:
        """Verify message integrity"""
        try:
            # Verify signature using constant-time comparison
            return hmac.compare_digest(
                message.signature.encode('utf-8'),
                self.generate_signature(message.payload).encode('utf-8')
            )
        except Exception:
            return False

    def process_message(self, message: SecureMessage) -> Any:
        """Process and verify message"""
        if not self.verify_message(message):
            raise ValueError("Message verification failed")
        
        try:
            return self.deserialize(message.payload)
        except ValueError:
            raise ValueError("Deserialization failed")

# Example usage
if __name__ == "__main__":
    # Generate a secure random key
    secret_key = os.urandom(32)
    
    # Initialize protocol
    protocol = SecureProtocol(secret_key)
    
    # Example data
    data = {"key": "value", "number": 42}
    
    # Create and send message
    message = protocol.create_message(data)
    print(f"Message: {message}")
    
    # Process message
    result = protocol.process_message(message)
    print(f"Processed result: {result}")