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
TIMEOUT = 30  # 30 seconds timeout

@dataclass
class SecureMessage:
    """Secure message container with timestamp and signature"""
    timestamp: float
    data: str
    signature: str

class SecureProtocol:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.last_timestamp = datetime.now().timestamp()

    def serialize(self, obj: Any) -> str:
        """Securely serialize object to JSON"""
        try:
            # Convert object to JSON
            json_data = json.dumps(obj, default=str)
            
            # Encode JSON to base64
            encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
            
            # Create timestamp
            timestamp = datetime.now().timestamp()
            
            # Create signature
            message = f"{timestamp}:{encoded_data}".encode('utf-8')
            signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
            
            # Create message object
            message_obj = SecureMessage(
                timestamp=timestamp,
                data=encoded_data,
                signature=signature
            )
            
            return json.dumps(message_obj.__dict__)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Serialization error: {str(e)}")

    def deserialize(self, data: str) -> Any:
        """Securely deserialize object from JSON"""
        try:
            message = json.loads(data)
            
            # Validate message structure
            if not isinstance(message, dict) or not all(key in message for key in ['timestamp', 'data', 'signature']):
                raise ValueError("Invalid message structure")
            
            # Verify signature
            message_str = f"{message['timestamp']}:{message['data']}".encode('utf-8')
            expected_signature = hmac.new(self.secret_key, message_str, hashlib.sha256).hexdigest()
            
            if not hmac.compare_digest(message['signature'], expected_signature):
                raise ValueError("Invalid signature")
            
            # Validate timestamp
            if message['timestamp'] < self.last_timestamp:
                raise ValueError("Invalid timestamp")
            
            # Decode data
            decoded_data = base64.b64decode(message['data'].encode('utf-8')).decode('utf-8')
            
            # Parse JSON
            return json.loads(decoded_data)
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            raise ValueError(f"Deserialization error: {str(e)}")

    def send_receive(self, obj: Any) -> Any:
        """Send and receive object with timeout"""
        start_time = datetime.now().timestamp()
        
        # Serialize
        serialized = self.serialize(obj)
        
        # Check size
        if len(serialized.encode('utf-8')) > MAX_MESSAGE_SIZE:
            raise ValueError("Message too large")
        
        # Send
        while datetime.now().timestamp() - start_time < TIMEOUT:
            try:
                # Simulating network send
                yield serialized
                break
            except Exception:
                continue
        
        raise TimeoutError("Send operation timed out")

    def receive(self) -> Any:
        """Receive and deserialize object with timeout"""
        try:
            serialized = next(self.send_receive(None))
            return self.deserialize(serialized)
        except TimeoutError:
            raise TimeoutError("Receive operation timed out")