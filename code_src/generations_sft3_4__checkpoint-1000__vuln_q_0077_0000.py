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
        # Convert to dictionary and then to JSON string
        data = profile.to_dict()
        # Use safe file path
        safe_path = Path(filename).resolve()
        # Ensure directory exists
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        # Write to file using safe JSON serialization
        with safe_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving profile: {e}")

def load_user_profile(filename: str) -> UserProfile:
    """Securely load user profile from file"""
    try:
        # Use safe file path
        safe_path = Path(filename).resolve()
        # Ensure file exists
        if not safe_path.is_file():
            raise FileNotFoundError(f"Profile file not found: {safe_path}")
        # Read file using safe JSON deserialization
        with safe_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        # Convert to UserProfile object
        return UserProfile.from_dict(data)
    except Exception as e:
        print(f"Error loading profile: {e}")
        return None