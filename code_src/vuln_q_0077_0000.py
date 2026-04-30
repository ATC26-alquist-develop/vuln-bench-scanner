import json
import os
from typing import Dict, Any

class SecureProfileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_profile(self, profile_data: Dict[str, Any]) -> None:
        """Securely save profile data using JSON."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(profile_data, f, indent=2)
        except IOError as e:
            print(f"Error saving profile: {e}")

    def load_profile(self) -> Dict[str, Any]:
        """Securely load profile data using JSON."""
        try:
            if not os.path.exists(self.file_path):
                return {}
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading profile: {e}")
            return {}

# Example usage
if __name__ == "__main__":
    manager = SecureProfileManager("user_profile.json")
    profile = {"username": "alice", "age": 30}
    manager.save_profile(profile)
    loaded_profile = manager.load_profile()
    print(loaded_profile)