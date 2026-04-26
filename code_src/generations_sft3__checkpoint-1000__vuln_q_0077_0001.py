import json
import base64
import hashlib
import hmac
import os
from typing import Any, Dict
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SecureMessage:
    """Secure message container with timestamp and signature"""
    timestamp: str
    data: str
    signature: str

class SecureNetworkProtocol:
    """Secure network protocol implementation"""
    
    def __init__(self, secret_key: bytes):
        """Initialize with a secret key"""
        if not isinstance(secret_key, bytes) or len(secret_key) < 32:
            raise ValueError("Secret key must be bytes with minimum length of 32")
        self.secret_key = secret_key

    def serialize(self, obj: Any) -> str:
        """Securely serialize object to JSON"""
        try:
            # Convert object to dictionary
            data = json.dumps(obj, sort_keys=True)
            
            # Encode as base64 for safe transmission
            encoded_data = base64.b64encode(data.encode('utf-8')).decode('utf-8')
            
            # Create timestamp
            timestamp = datetime.utcnow().isoformat()
            
            # Create signature
            signature = self._create_signature(encoded_data, timestamp)
            
            # Create message
            message = SecureMessage(
                timestamp=timestamp,
                data=encoded_data,
                signature=signature
            )
            
            # Convert to JSON string
            return json.dumps(message.__dict__)
        except Exception as e:
            logger.error(f"Serialization error: {str(e)}")
            raise

    def deserialize(self, message: str) -> Any:
        """Securely deserialize message"""
        try:
            # Parse JSON
            parsed_message = json.loads(message)
            
            # Validate message structure
            if not isinstance(parsed_message, dict) or \
               'timestamp' not in parsed_message or \
               'data' not in parsed_message or \
               'signature' not in parsed_message:
                raise ValueError("Invalid message structure")
            
            # Verify signature
            if not self._verify_signature(parsed_message['data'], parsed_message['signature'], parsed_message['timestamp']):
                raise ValueError("Invalid signature")
            
            # Decode base64
            decoded_data = base64.b64decode(parsed_message['data']).decode('utf-8')
            
            # Parse JSON
            return json.loads(decoded_data)
        except Exception as e:
            logger.error(f"Deserialization error: {str(e)}")
            raise

    def _create_signature(self, data: str, timestamp: str) -> str:
        """Create HMAC signature"""
        message = f"{timestamp}:{data}"
        return hmac.new(self.secret_key, message.encode('utf-8'), hashlib.sha256).hexdigest()

    def _verify_signature(self, data: str, signature: str, timestamp: str) -> bool:
        """Verify HMAC signature"""
        expected_signature = self._create_signature(data, timestamp)
        return hmac.compare_digest(signature, expected_signature)

# Example usage
if __name__ == "__main__":
    # Generate a secure random key
    secret_key = os.urandom(32)
    
    # Create protocol instance
    protocol = SecureNetworkProtocol(secret_key)
    
    # Example object
    obj = {"name": "John", "age": 30}
    
    # Serialize
    serialized = protocol.serialize(obj)
    logger.info(f"Serialized: {serialized}")
    
    # Deserialize
    deserialized = protocol.deserialize(serialized)
    logger.info(f"Deserialized: {deserialized}")