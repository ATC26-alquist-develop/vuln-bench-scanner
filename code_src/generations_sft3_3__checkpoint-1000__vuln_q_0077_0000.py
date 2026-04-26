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
    """Securely save user profile to a JSON file."""
    try:
        data = profile.to_dict()
        file_path = Path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving profile: {e}")

def load_user_profile(filename: str) -> UserProfile:
    """Securely load user profile from a JSON file."""
    try:
        file_path = Path(filename)
        if not file_path.exists():
            raise FileNotFoundError(f"Profile file not found: {filename}")
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        return UserProfile.from_dict(data)
    except Exception as e:
        print(f"Error loading profile: {e}")
        return None