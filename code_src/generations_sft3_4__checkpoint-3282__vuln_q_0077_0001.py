import json
import base64
import hmac
import hashlib
import os
from typing import Any, Dict
from dataclasses import dataclass
from datetime import datetime

# Secure configuration
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB limit
SECRET_KEY = os.urandom(32)  # Generate a random 32-byte key

@dataclass
class SecureMessage:
    """Secure message container with timestamp"""
    timestamp: str
    data: str

def serialize_secure(obj: Any) -> str:
    """Securely serialize object to JSON with timestamp"""
    try:
        # Convert object to JSON
        json_data = json.dumps(obj, default=str)
        
        # Add timestamp
        timestamp = datetime.utcnow().isoformat()
        
        # Combine data
        message = f"{timestamp}|{json_data}"
        
        # Encode as base64
        encoded = base64.b64encode(message.encode()).decode()
        
        return encoded
    except (TypeError, ValueError) as e:
        raise ValueError(f"Serialization error: {str(e)}")

def deserialize_secure(encoded: str) -> Dict:
    """Securely deserialize base64 encoded JSON"""
    try:
        # Decode base64
        decoded = base64.b64decode(encoded.encode()).decode()
        
        # Split and parse
        timestamp, json_data = decoded.split('|', 1)
        
        # Validate timestamp
        try:
            datetime.fromisoformat(timestamp)
        except ValueError:
            raise ValueError("Invalid timestamp format")
        
        # Parse JSON
        return json.loads(json_data)
    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError(f"Deserialization error: {str(e)}")

def sign_message(message: str) -> str:
    """Create HMAC signature for message"""
    try:
        return hmac.new(SECRET_KEY, message.encode(), hashlib.sha256).hexdigest()
    except Exception as e:
        raise ValueError(f"Signature creation error: {str(e)}")

def verify_signature(message: str, signature: str) -> bool:
    """Verify HMAC signature"""
    try:
        expected = sign_message(message)
        return hmac.compare_digest(signature, expected)
    except Exception:
        return False

def send_receive_secure(obj: Any) -> Dict:
    """Send and receive object securely"""
    try:
        # Serialize and sign
        encoded = serialize_secure(obj)
        signature = sign_message(encoded)
        
        # Send encoded message
        message = f"{encoded}|{signature}"
        
        # Receive and verify
        received = message.split('|', 1)
        if len(received) != 2:
            raise ValueError("Invalid message format")
        
        decoded = deserialize_secure(received[0])
        if not verify_signature(received[0], received[1]):
            raise ValueError("Invalid signature")
        
        return decoded
    
    except Exception as e:
        raise RuntimeError(f"Secure communication error: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        # Example object
        obj = {"name": "John", "age": 30}
        
        # Send and receive
        result = send_receive_secure(obj)
        print("Received:", result)
        
    except Exception as e:
        print(f"Error: {str(e)}")