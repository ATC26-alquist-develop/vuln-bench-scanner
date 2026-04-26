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
            raise SystemError("Failed to initialize Docker client")

    def _setup_logging(self) -> logging.Logger:
        """Configure secure logging"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        return logger

    def _validate_image_name(self, image_name: str) -> bool:
        """Validate image name format"""
        if not isinstance(image_name, str):
            return False
        # Only allow alphanumeric chars, dots, hyphens, and slashes
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$'
        return bool(re.match(pattern, image_name))

    def list_images(self) -> list[str]:
        """List available images securely"""
        try:
            return [img.tags[0] for img in self.client.images.list()]
        except docker.errors.DockerException as e:
            self.logger.error(f"Failed to list images: {str(e)}")
            raise SystemError("Failed to list images")

    def select_image(self, image_name: str) -> Optional[str]:
        """Securely select an image"""
        try:
            if not self._validate_image_name(image_name):
                self.logger.error(f"Invalid image name format: {image_name}")
                raise ValueError("Invalid image name format")
            
            if not image_name:
                raise ValueError("Image name cannot be empty")
                
            # Get image details
            image = self.client.images.get(image_name)
            return image.tags[0]
            
        except docker.errors.ImageNotFound:
            self.logger.error(f"Image not found: {image_name}")
            raise SystemError(f"Image '{image_name}' not found")
        except docker.errors.DockerException as e:
            self.logger.error(f"Failed to select image: {str(e)}")
            raise SystemError("Failed to select image")

def main():
    """Main function with secure execution"""
    try:
        manager = SecureDockerManager()
        images = manager.list_images()
        print("Available images:")
        for img in images:
            print(f"- {img}")
        
        # Example of secure image selection
        user_input = input("Enter image name to select: ").strip()
        selected_image = manager.select_image(user_input)
        print(f"Selected image: {selected_image}")
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        print("An error occurred. Please check logs for details.")

if __name__ == "__main__":
    main()