import json
import base64
import hmac
import hashlib
import secrets
from typing import Any, Dict
from dataclasses import dataclass
from datetime import datetime

# Secure configuration
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB limit
SECRET_KEY = secrets.token_bytes(32)  # 256-bit secret key

@dataclass
class SecureMessage:
    """Secure message container with timestamp"""
    timestamp: str
    payload: str

class SecureProtocol:
    """Secure network protocol implementation"""
    
    @staticmethod
    def serialize_object(obj: Any) -> str:
        """Securely serialize object to JSON"""
        try:
            # Convert object to JSON
            json_data = json.dumps(obj, default=str)
            
            # Encode to base64 for safe transport
            encoded_data = base64.b64encode(json_data.encode()).decode()
            
            # Create timestamp
            timestamp = datetime.utcnow().isoformat()
            
            # Create secure message
            secure_msg = SecureMessage(
                timestamp=timestamp,
                payload=encoded_data
            )
            
            # Sign the message
            signature = hmac.new(
                SECRET_KEY,
                secure_msg.json().encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Combine components
            return f"{secure_msg.json()}|{signature}"
            
        except (TypeError, ValueError) as e:
            raise ValueError(f"Serialization error: {str(e)}")

    @staticmethod
    def deserialize_object(data: str) -> Dict[str, Any]:
        """Securely deserialize object from JSON"""
        try:
            # Split components
            msg_str, signature = data.split('|')
            
            # Verify signature
            expected_sig = hmac.new(
                SECRET_KEY,
                msg_str.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_sig):
                raise ValueError("Invalid signature")
                
            # Parse JSON
            secure_msg = SecureMessage.parse_raw(msg_str)
            
            # Decode base64
            decoded_data = base64.b64decode(secure_msg.payload).decode()
            
            # Parse JSON
            return json.loads(decoded_data)
            
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Deserialization error: {str(e)}")

    @staticmethod
    def send_receive_object(obj: Any) -> Dict[str, Any]:
        """Send and receive object using secure protocol"""
        try:
            serialized = SecureProtocol.serialize_object(obj)
            
            # Simulate sending/receiving (replace with actual network code)
            received = serialized
            
            return SecureProtocol.deserialize_object(received)
            
        except Exception as e:
            raise RuntimeError(f"Protocol error: {str(e)}")