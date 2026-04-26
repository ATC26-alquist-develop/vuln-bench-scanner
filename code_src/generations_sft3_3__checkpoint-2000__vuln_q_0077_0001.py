import json
import base64
import hmac
import hashlib
import os
from typing import Any, Dict
from dataclasses import dataclass
from enum import Enum, auto

class MessageType(Enum):
    """Valid message types"""
    REQUEST = auto()
    RESPONSE = auto()

@dataclass
class SecureMessage:
    """Secure message container with validation"""
    message_type: MessageType
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
            
            # Create final message
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
            
            # Validate message structure
            if not isinstance(parsed, dict):
                raise ValueError("Invalid message format")
            
            # Validate message type
            message_type = parsed.get('message_type')
            if not isinstance(message_type, str):
                raise ValueError("Invalid message type")
            message_type = MessageType[message_type.upper()]
            
            # Validate payload
            payload = parsed.get('payload')
            if not isinstance(payload, str):
                raise ValueError("Invalid payload format")
            
            # Validate signature
            signature = parsed.get('signature')
            if not isinstance(signature, str):
                raise ValueError("Invalid signature format")
            
            # Verify signature
            expected_signature = hmac.new(
                self.secret_key,
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            if not hmac.compare_digest(signature, expected_signature):
                raise ValueError("Invalid signature")
            
            # Deserialize payload
            decoded_payload = base64.b64decode(payload).decode('utf-8')
            payload_dict = json.loads(decoded_payload)
            
            return SecureMessage(
                message_type=message_type,
                payload=payload_dict,
                signature=signature
            )
        except Exception as e:
            raise ValueError(f"Deserialization failed: {str(e)}")

    def send_receive(self, message: SecureMessage) -> SecureMessage:
        """Send and receive message"""
        serialized = self.serialize(message)
        # Simulated network send/receive
        received = self.deserialize(serialized)
        return received