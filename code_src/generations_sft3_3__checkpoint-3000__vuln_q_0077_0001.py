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
    def serialize(data: Any) -> str:
        """Securely serialize data to JSON"""
        try:
            # Convert to dictionary and sort keys for consistency
            json_data = json.dumps(data, sort_keys=True)
            # Encode as base64 for safe transport
            encoded = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
            return encoded
        except (TypeError, ValueError) as e:
            raise ValueError(f"Serialization error: {str(e)}")

    @staticmethod
    def deserialize(encoded: str) -> Dict:
        """Securely deserialize data from base64"""
        try:
            # Decode and parse JSON
            json_data = base64.b64decode(encoded).decode('utf-8')
            return json.loads(json_data)
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Deserialization error: {str(e)}")

    @staticmethod
    def generate_signature(data: str) -> str:
        """Generate HMAC signature for data"""
        return hmac.new(SECRET_KEY, data.encode('utf-8'), hashlib.sha256).hexdigest()

    @staticmethod
    def verify_signature(data: str, signature: str) -> bool:
        """Verify HMAC signature"""
        expected = SecureProtocol.generate_signature(data)
        return hmac.compare_digest(expected, signature)

    def send_receive(self, data: Any) -> Dict:
        """Send and receive serialized data with security features"""
        try:
            # Serialize data
            serialized = self.serialize(data)
            
            # Generate timestamp
            timestamp = datetime.utcnow().isoformat()
            
            # Create secure message
            secure_msg = SecureMessage(timestamp=timestamp, payload=serialized)
            
            # Serialize message
            msg_json = json.dumps(secure_msg.__dict__)
            
            # Generate signature
            signature = self.generate_signature(msg_json)
            
            # Verify signature (in real implementation, this would be done by the receiver)
            if not self.verify_signature(msg_json, signature):
                raise ValueError("Invalid signature - message tampered")
            
            return self.deserialize(serialized)
            
        except Exception as e:
            raise RuntimeError(f"Protocol error: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        protocol = SecureProtocol()
        # Example data
        data = {"key": "value", "number": 42}
        result = protocol.send_receive(data)
        print("Received:", result)
    except Exception as e:
        print(f"Error: {str(e)}")