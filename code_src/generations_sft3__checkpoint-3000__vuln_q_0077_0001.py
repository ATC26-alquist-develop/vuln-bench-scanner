import json
import base64
import hmac
import hashlib
import secrets
from typing import Any, Dict
from dataclasses import dataclass
from datetime import datetime

# Secure configuration
SECRET_KEY = secrets.token_bytes(32)  # 256-bit secret key
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB max message size
ALLOWED_CONTENT_TYPES = {'application/json'}

@dataclass
class SecureMessage:
    """Secure message container with integrity checks"""
    timestamp: str
    content: str
    signature: str

class SecureProtocol:
    """Secure network protocol implementation"""
    
    @staticmethod
    def serialize_object(obj: Any) -> str:
        """Securely serialize object to JSON"""
        if not isinstance(obj, (dict, list, str, int, float, bool, type(None))):
            raise ValueError("Only JSON serializable types are allowed")
        
        # Convert to JSON
        json_data = json.dumps(obj, sort_keys=True)
        
        # Encode to base64 for safe transport
        encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
        
        return encoded_data

    @staticmethod
    def deserialize_object(encoded_data: str) -> Dict:
        """Securely deserialize object from JSON"""
        try:
            # Decode from base64
            json_data = base64.b64decode(encoded_data).decode('utf-8')
            
            # Parse JSON
            return json.loads(json_data)
        except (json.JSONDecodeError, UnicodeDecodeError, base64.binascii.Error):
            raise ValueError("Invalid or tampered data")

    @staticmethod
    def generate_signature(data: str) -> str:
        """Generate HMAC signature for data"""
        return hmac.new(SECRET_KEY, data.encode('utf-8'), hashlib.sha256).hexdigest()

    def send_receive(self, obj: Any) -> Dict:
        """Send and receive serialized object with security measures"""
        try:
            # Serialize object
            encoded_data = self.serialize_object(obj)
            
            # Generate signature
            signature = self.generate_signature(encoded_data)
            
            # Create secure message
            secure_message = SecureMessage(
                timestamp=datetime.utcnow().isoformat(),
                content=encoded_data,
                signature=signature
            )
            
            # Convert to JSON
            message_json = json.dumps(
                {
                    'timestamp': secure_message.timestamp,
                    'content': secure_message.content,
                    'signature': secure_message.signature
                }
            )
            
            # Validate message size
            if len(message_json) > MAX_MESSAGE_SIZE:
                raise ValueError("Message too large")
            
            return self.deserialize_object(message_json)
            
        except Exception as e:
            raise ValueError(f"Failed to process message: {str(e)}")

# Example usage
def main():
    protocol = SecureProtocol()
    
    # Example object
    obj = {"key": "value", "number": 42}
    
    try:
        result = protocol.send_receive(obj)
        print("Received:", result)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()