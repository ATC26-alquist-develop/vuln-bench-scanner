import docker
import re
import logging
from typing import Optional
from pathlib import Path

class SecureDockerManager:
    def __init__(self, timeout: int = 30):
        """Initialize Docker manager with security controls"""
        self.timeout = timeout
        self.client = self._create_secure_client()
        self.logger = self._setup_logging()
        
    def _create_secure_client(self) -> docker.DockerClient:
        """Create Docker client with security controls"""
        try:
            return docker.from_env(timeout=self.timeout)
        except docker.errors.DockerException as e:
            self.logger.error(f"Docker client initialization failed: {str(e)}")
            raise RuntimeError("Failed to initialize Docker client")

    def _setup_logging(self) -> logging.Logger:
        """Configure secure logging"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        return logger

    def _validate_image_name(self, image_name: str) -> bool:
        """Validate image name format"""
        if not image_name or len(image_name) > 256:
            return False
        
        # Only allow alphanumeric chars, dots, dashes, and slashes
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]{0,255}$'
        return bool(re.match(pattern, image_name))

    def get_image_info(self, image_name: str) -> Optional[dict]:
        """
        Securely get image information
        Returns None if validation fails or error occurs
        """
        try:
            if not self._validate_image_name(image_name):
                self.logger.warning(f"Invalid image name format: {image_name}")
                return None

            image = self.client.images.get(image_name)
            return {
                'Id': image.id,
                'Created': image.created,
                'ParentId': image.parent_id,
                'RepoTags': image.tags
            }
        except docker.errors.ImageNotFound:
            self.logger.warning(f"Image not found: {image_name}")
            return None
        except Exception as e:
            self.logger.error(f"Error getting image info: {str(e)}")
            return None

    def list_images(self) -> list:
        """Securely list all images"""
        try:
            return [img.tags for img in self.client.images.list()]
        except Exception as e:
            self.logger.error(f"Error listing images: {str(e)}")
            return []

def main():
    """Main function with secure input handling"""
    try:
        manager = SecureDockerManager()
        
        # Get user input with validation
        image_name = input("Enter image name: ").strip()
        if not image_name:
            print("Invalid input")
            return

        # Get image info
        info = manager.get_image_info(image_name)
        if info:
            print(f"Image info: {info}")
        else:
            print("Failed to get image info")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()