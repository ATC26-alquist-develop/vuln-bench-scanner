import docker
import re
import os
import logging
from typing import Optional
from pathlib import Path

class SecureDockerManager:
    def __init__(self):
        # Initialize Docker client with timeout and TLS verification
        self.client = docker.from_env(timeout=30, 
                                 version='auto',
                                 tls=True,
                                 assert_hostname=True)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _validate_image_name(self, image_name: str) -> bool:
        """Validate Docker image name format."""
        # Only allow alphanumeric chars, dots, dashes, and slashes
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]+[a-zA-Z0-9]$'
        return bool(re.match(pattern, image_name))

    def _validate_path(self, path: str) -> bool:
        """Validate file path exists and is within allowed directory."""
        try:
            path_obj = Path(path).resolve()
            # Ensure path is within current working directory
            return path_obj.is_file() and str(path_obj).startswith(os.getcwd())
        except (ValueError, RuntimeError):
            return False

    def select_image(self, image_name: str) -> Optional[str]:
        """Securely select a Docker image."""
        try:
            # Validate input
            if not self._validate_image_name(image_name):
                self.logger.error("Invalid image name format")
                return None

            # Check if image exists
            image = self.client.images.get(image_name)
            if not image:
                self.logger.error(f"Image {image_name} not found")
                return None

            # Validate image path if it's a local image
            if image.tags:
                image_path = image.tags[0]
                if not self._validate_path(image_path):
                    self.logger.error(f"Invalid image path: {image_path}")
                    return None

            return image_name

        except docker.errors.ImageNotFound:
            self.logger.error(f"Image not found: {image_name}")
            return None
        except Exception as e:
            self.logger.error(f"Error selecting image: {str(e)}")
            return None

    def run_container(self, image_name: str) -> Optional[docker.models.containers.Container]:
        """Securely run a container from the selected image."""
        try:
            image = self.select_image(image_name)
            if not image:
                return None

            # Create container with security options
            container = self.client.containers.run(
                image,
                detach=True,
                remove=True,
                network_mode='none',
                cap_drop=['ALL'],
                security_opt=['no-new-privileges:true']
            )
            return container

        except Exception as e:
            self.logger.error(f"Error running container: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    manager = SecureDockerManager()
    container = manager.run_container("nginx:latest")
    if container:
        print(f"Container started: {container.id}")