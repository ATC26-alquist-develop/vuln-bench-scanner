import json
import base64
import hashlib
import hmac
import os
from typing import Any, Dict
from dataclasses import dataclass
from datetime import datetime

# Secure configuration
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB limit
SECRET_KEY = os.urandom(32)  # Generate a random 32-byte key

@dataclass
class SecureMessage:
    """Secure message container with timestamp and signature"""
    timestamp: float
    data: Dict[str, Any]
    signature: str

def serialize_object(obj: Any) -> str:
    """Securely serialize an object to JSON"""
    try:
        # Convert object to dictionary
        obj_dict = obj.__dict__
        # Convert dictionary to JSON
        json_data = json.dumps(obj_dict)
        # Encode JSON to base64
        encoded_data = base64.b64encode(json_data.encode()).decode()
        return encoded_data
    except Exception as e:
        raise ValueError(f"Serialization error: {str(e)}")

def deserialize_object(encoded_data: str) -> Dict[str, Any]:
    """Securely deserialize JSON to object"""
    try:
        # Decode base64
        json_data = base64.b64decode(encoded_data).decode()
        # Parse JSON
        obj_dict = json.loads(json_data)
        # Convert dictionary to object
        return obj_dict
    except Exception as e:
        raise ValueError(f"Deserialization error: {str(e)}")

def create_secure_message(obj: Any) -> SecureMessage:
    """Create a secure message with timestamp and signature"""
    try:
        # Serialize object
        encoded_data = serialize_object(obj)
        # Create timestamp
        timestamp = datetime.utcnow().timestamp()
        # Create signature
        signature = hmac.new(SECRET_KEY, encoded_data.encode(), hashlib.sha256).hexdigest()
        # Create message
        return SecureMessage(timestamp=timestamp, data=encoded_data, signature=signature)
    except Exception as e:
        raise ValueError(f"Message creation error: {str(e)}")

def verify_secure_message(message: SecureMessage, obj: Any) -> bool:
    """Verify the integrity of a secure message"""
    try:
        # Deserialize data
        decoded_data = deserialize_object(message.data)
        # Verify signature
        expected_signature = hmac.new(SECRET_KEY, message.data.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(message.signature, expected_signature)
    except Exception as e:
        return False

def send_secure_message(message: SecureMessage) -> str:
    """Send a secure message"""
    try:
        # Verify message integrity
        if not verify_secure_message(message, message.data):
            raise ValueError("Message integrity check failed")
        
        # Encode message for transmission
        encoded_message = json.dumps({
            "timestamp": message.timestamp,
            "data": message.data,
            "signature": message.signature
        }).encode()
        
        # Return encoded message
        return base64.b64encode(encoded_message).decode()
    except Exception as e:
        raise ValueError(f"Message sending error: {str(e)}")

def receive_secure_message(encoded_message: str) -> SecureMessage:
    """Receive and verify a secure message"""
    try:
        # Decode message
        decoded_message = base64.b64decode(encoded_message.encode())
        # Parse JSON
        message_data = json.loads(decoded_message)
        
        # Verify message integrity
        if not verify_secure_message(SecureMessage(**message_data), message_data['data']):
            raise ValueError("Message integrity check failed")
        
        return SecureMessage(**message_data)
    except Exception as e:
        raise ValueError(f"Message receiving error: {str(e)}")