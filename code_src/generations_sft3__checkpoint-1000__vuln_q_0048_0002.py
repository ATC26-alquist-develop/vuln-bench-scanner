import docker
import re
import os
from typing import Optional
from pathlib import Path

class SecureDockerManager:
    def __init__(self):
        # Initialize Docker client with TLS verification
        self.client = docker.from_env()
        
    def validate_image_name(self, image_name: str) -> bool:
        """Validate Docker image name format."""
        # Only allow alphanumeric chars, hyphens, dots, and slashes
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]$'
        return bool(re.match(pattern, image_name))
    
    def get_image_info(self, image_name: str) -> Optional[dict]:
        """Safely get image information."""
        try:
            # Validate image name
            if not self.validate_image_name(image_name):
                raise ValueError("Invalid image name format")
            
            # Get image info
            image = self.client.images.get(image_name)
            return {
                'name': image.tags[0],
                'id': image.id,
                'size': image.attrs['Size'],
                'created': image.attrs['Created']
            }
        except docker.errors.ImageNotFound:
            return None
        except Exception as e:
            # Log error but don't expose details
            return None

    def list_images(self) -> list:
        """Safely list all available images."""
        try:
            return [img.tags[0] for img in self.client.images.list()]
        except Exception:
            return []

def main():
    # Initialize manager
    manager = SecureDockerManager()
    
    while True:
        print("\n1. List images")
        print("2. Get image info")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            images = manager.list_images()
            print("Available images:")
            for img in images:
                print(f"- {img}")
        elif choice == '2':
            image_name = input("Enter image name: ")
            info = manager.get_image_info(image_name)
            if info:
                print(f"Image info for {info['name']}:")
                print(f"ID: {info['id']}")
                print(f"Size: {info['size']} bytes")
                print(f"Created: {info['created']}")
            else:
                print("Failed to retrieve image info")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()