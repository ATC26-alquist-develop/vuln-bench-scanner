import json
from typing import Any
import hashlib
import hmac
import os

class SecureDataSerializer:
    def __init__(self, secret_key: bytes):
        """Initialize with a secret key for data integrity."""
        if not isinstance(secret_key, bytes) or len(secret_key) < 32:
            raise ValueError("Secret key must be bytes with at least 32 bytes length")
        self.secret_key = secret_key

    def serialize(self, data: Any) -> str:
        """Securely serialize data to JSON string with integrity."""
        try:
            # Convert data to JSON, handling complex types
            json_data = json.dumps(data, default=self._json_serializer)
            
            # Create HMAC for integrity
            hmac_digest = self._create_hmac(json_data)
            
            # Combine data and HMAC
            return f"{json_data}|{hmac_digest}"
        except (TypeError, ValueError) as e:
            raise ValueError(f"Serialization failed: {str(e)}")

    def deserialize(self, serialized_data: str) -> Any:
        """Securely deserialize JSON string with integrity check."""
        try:
            # Split data and HMAC
            parts = serialized_data.split('|')
            if len(parts) != 2:
                raise ValueError("Invalid serialized data format")
            
            json_data, received_hmac = parts
            
            # Verify HMAC
            if not self._verify_hmac(json_data, received_hmac):
                raise ValueError("Data integrity check failed")
            
            # Parse JSON and return the data
            return json.loads(json_data)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Deserialization failed: {str(e)}")

    def _json_serializer(self, obj: Any) -> dict:
        """Custom JSON serializer for complex types."""
        if isinstance(obj, (datetime, date)):
            return {"__type__": type(obj).__name__, "value": obj.isoformat()}
        raise TypeError(f"Type {type(obj)} not serializable")

    def _create_hmac(self, message: str) -> str:
        """Create HMAC for data integrity."""
        return hmac.new(
            self.secret_key,
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _verify_hmac(self, message: str, received_hmac: str) -> bool:
        """Verify HMAC for data integrity."""
        expected_hmac = self._create_hmac(message)
        return hmac.compare_digest(
            expected_hmac.encode('utf-8'),
            received_hmac.encode('utf-8')
        )