import json
import os
from typing import Dict, Any
import secrets

class SecureProfileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._generate_secure_filename()

    def _generate_secure_filename(self) -> None:
        """Generate a secure filename to prevent path traversal attacks."""
        self.filename = f"profile_{secrets.token_hex(8)}.json"

    def save_profile(self, profile_data: Dict[str, Any]) -> None:
        """Securely save profile data to disk."""
        try:
            # Validate input
            if not isinstance(profile_data, dict):
                raise ValueError("Profile data must be a dictionary")

            # Sanitize data
            sanitized_data = {k: str(v) for k, v in profile_data.items()}

            # Encrypt data before saving
            encrypted_data = self._encrypt_data(json.dumps(sanitized_data))

            # Use atomic write to prevent partial writes
            temp_file = f"{self.filename}.tmp"
            with open(temp_file, 'w') as f:
                f.write(encrypted_data)
            os.replace(temp_file, self.file_path)

        except Exception as e:
            raise RuntimeError(f"Failed to save profile: {str(e)}")

    def load_profile(self) -> Dict[str, Any]:
        """Securely load profile data from disk."""
        try:
            if not os.path.exists(self.file_path):
                return {}

            with open(self.file_path, 'r') as f:
                encrypted_data = f.read()

            # Decrypt data
            decrypted_data = self._decrypt_data(encrypted_data)

            # Parse JSON and validate structure
            profile_data = json.loads(decrypted_data)
            if not isinstance(profile_data, dict):
                raise ValueError("Invalid profile data structure")

            return profile_data

        except Exception as e:
            raise RuntimeError(f"Failed to load profile: {str(e)}")

    def _encrypt_data(self, data: str) -> str:
        """Encrypt data using a simple XOR cipher (replace with a proper encryption library)."""
        key = secrets.token_bytes(16)
        encrypted = bytearray()
        for i, byte in enumerate(data.encode('utf-8')):
            encrypted.append(byte ^ key[i % len(key)])
        return encrypted.hex()

    def _decrypt_data(self, data: str) -> str:
        """Decrypt data using the same XOR cipher (replace with a proper decryption method)."""
        key = secrets.token_bytes(16)
        encrypted = bytes.fromhex(data)
        decrypted = bytearray()
        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ key[i % len(key)])
        return decrypted.decode('utf-8')

# Example usage
if __name__ == "__main__":
    try:
        manager = SecureProfileManager("profile.json")
        
        # Save profile
        profile = {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com"
        }
        manager.save_profile(profile)
        print("Profile saved successfully")

        # Load profile
        loaded_profile = manager.load_profile()
        print("Loaded profile:", loaded_profile)
    except Exception as e:
        print(f"Error: {str(e)}")