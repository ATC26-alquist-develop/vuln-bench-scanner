import json
import base64
import hmac
import hashlib
import secrets
from typing import Any, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta

# Secure configuration
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB limit
SECRET_KEY = secrets.token_bytes(32)  # 256-bit secret key
TIMEOUT = 300  # 5 minutes timeout

@dataclass
class SecureMessage:
    """Secure message container with validation"""
    timestamp: str
    payload: str
    signature: str

class SecureProtocol:
    """Secure network protocol implementation"""
    
    def __init__(self):
        self.last_timestamp = datetime.utcnow()
        self.timeout = TIMEOUT

    def serialize(self, obj: Any) -> str:
        """Securely serialize object to JSON"""
        try:
            # Convert to dictionary and sort keys
            data = json.dumps(obj, sort_keys=True)
            
            # Encode to base64 for safe transport
            encoded = base64.b64encode(data.encode('utf-8')).decode('utf-8')
            
            # Create signature
            signature = self._create_signature(encoded)
            
            return f"{encoded}|{signature}"
        except Exception as e:
            raise ValueError(f"Serialization failed: {str(e)}")

    def deserialize(self, data: str) -> Any:
        """Securely deserialize object from JSON"""
        try:
            # Split data
            encoded, signature = data.split('|')
            
            # Verify signature
            if not self._verify_signature(encoded, signature):
                raise ValueError("Invalid signature")
                
            # Decode and parse JSON
            data = base64.b64decode(encoded).decode('utf-8')
            return json.loads(data)
        except Exception as e:
            raise ValueError(f"Deserialization failed: {str(e)}")

    def _create_signature(self, data: str) -> str:
        """Create HMAC signature"""
        timestamp = datetime.utcnow().isoformat()
        message = f"{timestamp}|{data}".encode('utf-8')
        return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

    def _verify_signature(self, data: str, signature: str) -> bool:
        """Verify HMAC signature"""
        try:
            timestamp = data[:29]  # ISO 8601 format
            message = data[30:]  # Remaining data
            
            expected_sig = self._create_signature(message)
            return hmac.compare_digest(signature, expected_sig)
        except Exception:
            return False

    def send_receive(self, obj: Any) -> Any:
        """Send and receive object with timeout"""
        if not isinstance(obj, (str, dict, list, int, float, bool, type(None))):
            raise ValueError("Unsupported object type")
            
        if len(obj) > MAX_MESSAGE_SIZE:
            raise ValueError("Message too large")

        start_time = datetime.utcnow()
        
        serialized = self.serialize(obj)
        
        # Check timeout
        if (datetime.utcnow() - start_time) > timedelta(seconds=self.timeout):
            raise TimeoutError("Operation timed out")

        # Simulate sending/receiving (replace with actual network code)
        return self.deserialize(serialized)