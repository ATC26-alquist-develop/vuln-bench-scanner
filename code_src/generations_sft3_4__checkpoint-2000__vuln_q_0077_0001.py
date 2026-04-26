import json
import base64
import hmac
import hashlib
import os
from typing import Any, Dict
from dataclasses import dataclass
from enum import Enum, auto

class SecureMessageType(Enum):
    """Enum for secure message types"""
    HELLO = auto()
    DATA = auto()
    ERROR = auto()

@dataclass
class SecureMessage:
    """Secure message class with validation"""
    message_type: SecureMessageType
    payload: Dict[str, Any]
    signature: str

class SecureProtocol:
    """Secure network protocol implementation"""
    
    def __init__(self, secret_key: bytes):
        """Initialize with a secret key"""
        if not isinstance(secret_key, bytes) or len(secret_key) < 32:
            raise ValueError("Secret key must be bytes with minimum length of 32")
        self.secret_key = secret_key

    def serialize(self, message: SecureMessage) -> str:
        """Securely serialize message"""
        try:
            # Serialize payload to JSON
            payload_str = json.dumps(message.payload)
            
            # Encode payload
            encoded_payload = base64.b64encode(payload_str.encode('utf-8')).decode('utf-8')
            
            # Create signature
            signature = hmac.new(
                self.secret_key,
                encoded_payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Create and return secure message
            return json.dumps({
                'message_type': message.message_type.name,
                'payload': encoded_payload,
                'signature': signature
            })
        except Exception as e:
            raise ValueError(f"Serialization failed: {str(e)}")

    def deserialize(self, data: str) -> SecureMessage:
        """Securely deserialize message"""
        try:
            # Parse JSON
            parsed = json.loads(data)
            
            # Validate message type
            if not isinstance(parsed.get('message_type'), str):
                raise ValueError("Invalid message type")
            
            # Validate payload
            if not isinstance(parsed.get('payload'), str):
                raise ValueError("Invalid payload")
            
            # Validate signature
            if not isinstance(parsed.get('signature'), str):
                raise ValueError("Invalid signature")
            
            # Verify signature
            expected_signature = hmac.new(
                self.secret_key,
                parsed['payload'].encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(
                parsed['signature'].encode('utf-8'),
                expected_signature.encode('utf-8')
            ):
                raise ValueError("Invalid signature")
            
            # Deserialize payload
            payload = json.loads(base64.b64decode(parsed['payload']).decode('utf-8'))
            
            return SecureMessage(
                message_type=SecureMessageType[parsed['message_type']],
                payload=payload,
                signature=parsed['signature']
            )
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        except Exception as e:
            raise ValueError(f"Deserialization failed: {str(e)}")

    def send(self, message: SecureMessage) -> str:
        """Send serialized message"""
        return self.serialize(message)

    def receive(self, data: str) -> SecureMessage:
        """Receive and deserialize message"""
        return self.deserialize(data)