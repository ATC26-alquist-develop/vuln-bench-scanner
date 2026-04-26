import json
from pathlib import Path
from typing import Dict, Any

class UserProfile:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        return cls(username=data['username'], email=data['email'])

def save_user_profile(profile: UserProfile, filename: str) -> None:
    """Securely save user profile to file"""
    try:
        # Use Path for safe file handling
        path = Path(filename)
        # Ensure the file is in a safe directory
        path.parent.mkdir(parents=True, exist_ok=True)
        # Use json.dump instead of pickle
        with path.open('w', encoding='utf-8') as f:
            json.dump(profile.to_dict(), f, indent=2)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error saving profile: {e}")

def load_user_profile(filename: str) -> UserProfile:
    """Securely load user profile from file"""
    try:
        # Use Path for safe file handling
        path = Path(filename)
        # Ensure the file exists and is a regular file
        if not path.is_file():
            raise FileNotFoundError(f"Profile file not found: {filename}")
        # Use json.load instead of pickle
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        # Validate loaded data
        if not isinstance(data, dict):
            raise ValueError("Invalid profile data format")
        return UserProfile.from_dict(data)
    except (IOError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading profile: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Create a user profile
    user = UserProfile("alice", "alice@example.com")
    
    # Save the profile
    save_user_profile(user, "user_profile.json")
    
    # Load the profile
    loaded_user = load_user_profile("user_profile.json")
    if loaded_user:
        print(f"Loaded user: {loaded_user.username}, {loaded_user.email}")