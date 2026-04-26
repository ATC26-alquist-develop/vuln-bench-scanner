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
    """Secure message container with timestamp"""
    timestamp: datetime
    data: Dict[str, Any]

class SecureProtocol:
    """Secure network protocol implementation"""
    
    def __init__(self):
        self.secret_key = SECRET_KEY

    def serialize(self, obj: Any) -> str:
        """Securely serialize object to JSON"""
        try:
            # Convert object to JSON
            json_data = json.dumps(obj, sort_keys=True)
            
            # Encode JSON to base64
            encoded = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
            
            # Create HMAC for integrity
            hmac_obj = hmac.new(self.secret_key, encoded.encode('utf-8'), hashlib.sha256)
            hmac_digest = hmac_obj.hexdigest()
            
            # Combine data and HMAC
            return f"{encoded}|{hmac_digest}"
        except Exception as e:
            raise ValueError(f"Serialization failed: {str(e)}")

    def deserialize(self, data: str) -> Dict[str, Any]:
        """Securely deserialize JSON data"""
        try:
            # Split data into encoded and HMAC
            encoded, hmac_digest = data.split('|')
            
            # Verify HMAC
            hmac_obj = hmac.new(self.secret_key, encoded.encode('utf-8'), hashlib.sha256)
            if not hmac.compare_digest(hmac_obj.hexdigest(), hmac_digest):
                raise ValueError("HMAC verification failed")
            
            # Decode and parse JSON
            json_data = base64.b64decode(encoded).decode('utf-8')
            return json.loads(json_data)
        except Exception as e:
            raise ValueError(f"Deserialization failed: {str(e)}")

    def send(self, data: Any) -> str:
        """Send serialized data"""
        return self.serialize(data)

    def receive(self, data: str) -> Dict[str, Any]:
        """Receive and deserialize data"""
        return self.deserialize(data)

# Example usage
if __name__ == "__main__":
    protocol = SecureProtocol()
    
    # Example object
    obj = {"name": "John", "age": 30, "data": [1, 2, 3]}
    
    # Send
    serialized = protocol.send(obj)
    print("Sent:", serialized)
    
    # Receive
    received = protocol.receive(serialized)
    print("Received:", received)