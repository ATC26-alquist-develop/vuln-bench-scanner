import json
import os
from typing import Dict, Any

class UserProfile:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def to_dict(self) -> Dict[str, Any]:
        return {
            'username': self.username,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        return cls(username=data['username'], email=data['email'])

class UserProfileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_profile(self, profile: UserProfile) -> None:
        try:
            data = profile.to_dict()
            with open(self.file_path, 'w') as f:
                json.dump(data, f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error saving profile: {e}")

    def load_profile(self) -> UserProfile:
        try:
            if not os.path.exists(self.file_path):
                return None
                
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            return UserProfile.from_dict(data)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading profile: {e}")
            return None