import json
import os
from typing import Dict, Any

class UserProfileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_profile(self, profile: Dict[str, Any]) -> None:
        """Securely save a user profile to a JSON file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(profile, f, indent=2)
        except IOError as e:
            print(f"Error saving profile: {e}")

    def load_profile(self) -> Dict[str, Any]:
        """Securely load a user profile from a JSON file."""
        try:
            if not os.path.exists(self.file_path):
                return {}
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}
        except IOError as e:
            print(f"Error loading profile: {e}")
            return {}

# Example usage
if __name__ == "__main__":
    manager = UserProfileManager("user_profile.json")
    
    # Save a profile
    user_profile = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }
    manager.save_profile(user_profile)
    
    # Load a profile
    loaded_profile = manager.load_profile()
    print(loaded_profile)