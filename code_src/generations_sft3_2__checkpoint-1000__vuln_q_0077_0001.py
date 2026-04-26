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
            
        except (TypeError, ValueError) as e:
            raise ValueError(f"Serialization failed: {str(e)}")

    def deserialize(self, data: str) -> Any:
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
            
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Deserialization failed: {str(e)}")

    def send(self, data: Any) -> str:
        """Send serialized data"""
        if not isinstance(data, (dict, list, str, int, float, bool, type(None))):
            raise ValueError("Invalid data type")
            
        if len(data) > MAX_MESSAGE_SIZE:
            raise ValueError("Message exceeds maximum size limit")
            
        return self.serialize(data)

    def receive(self, data: str) -> Any:
        """Receive and deserialize data"""
        try:
            return self.deserialize(data)
        except ValueError as e:
            raise ValueError(f"Received data is invalid: {str(e)}")

# Example usage
if __name__ == "__main__":
    protocol = SecureProtocol()
    
    # Sending data
    try:
        message = protocol.send({"key": "value", "number": 42})
        print("Sent message:", message)
    except ValueError as e:
        print(f"Error sending message: {str(e)}")
    
    # Receiving data
    try:
        received = protocol.receive(message)
        print("Received data:", received)
    except ValueError as e:
        print(f"Error receiving data: {str(e)}")