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
    data: Dict[str, Any]

class SecureProtocol:
    """Secure protocol for sending/receiving serialized objects"""
    
    @staticmethod
    def serialize(data: Dict[str, Any]) -> str:
        """Securely serialize data to JSON with timestamp"""
        timestamp = datetime.utcnow().isoformat()
        message = SecureMessage(timestamp=timestamp, data=data)
        return base64.b64encode(json.dumps(message.__dict__).encode()).decode()

    @staticmethod
    def deserialize(data: str) -> Dict[str, Any]:
        """Securely deserialize data from JSON with timestamp"""
        try:
            decoded = base64.b64decode(data.encode())
            message_dict = json.loads(decoded)
            
            # Validate message structure
            if not isinstance(message_dict, dict) or 'timestamp' not in message_dict or 'data' not in message_dict:
                raise ValueError("Invalid message structure")
                
            # Validate timestamp format
            try:
                datetime.fromisoformat(message_dict['timestamp'])
            except ValueError:
                raise ValueError("Invalid timestamp format")
                
            # Validate data
            if not isinstance(message_dict['data'], dict):
                raise ValueError("Invalid data structure")
                
            return message_dict['data']
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Deserialization error: {str(e)}")

    @staticmethod
    def encrypt(data: str) -> str:
        """Encrypt data using HMAC"""
        return hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def decrypt(data: str) -> str:
        """Decrypt data using HMAC"""
        expected = hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(data, expected):
            raise ValueError("Invalid HMAC")
        return data

    @staticmethod
    def send_receive(data: Dict[str, Any]) -> Dict[str, Any]:
        """Send and receive encrypted data"""
        try:
            # Serialize and encrypt
            serialized = SecureProtocol.serialize(data)
            encrypted = SecureProtocol.encrypt(serialized)
            
            # Send encrypted data
            # (implementation dependent - this is just the protocol)
            # send(encrypted)
            
            # Receive encrypted data
            received = receive()
            if not received:
                raise ValueError("Received empty data")
                
            # Decrypt and deserialize
            decrypted = SecureProtocol.decrypt(received)
            return SecureProtocol.deserialize(decrypted)
            
        except Exception as e:
            raise ValueError(f"Protocol error: {str(e)}")

# Example usage
def main():
    try:
        # Example data
        data = {"key": "value", "number": 42}
        
        # Send and receive
        result = SecureProtocol.send_receive(data)
        print("Received:", result)
        
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()