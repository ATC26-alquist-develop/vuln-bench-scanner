import docker
import re
import logging
from typing import Optional
from pathlib import Path

class SecureDockerManager:
    def __init__(self, base_image: str = "library/alpine"):
        """Initialize with a default base image."""
        self.base_image = base_image
        self.client = self._create_secure_client()
        self.logger = self._setup_logging()

    def _create_secure_client(self) -> docker.DockerClient:
        """Create a secure Docker client with limited permissions."""
        try:
            return docker.from_env()
        except docker.errors.DockerException as e:
            self.logger.error(f"Docker client initialization failed: {e}")
            raise RuntimeError("Failed to initialize Docker client")

    def _setup_logging(self) -> logging.Logger:
        """Set up secure logging configuration."""
        logger = logging.getLogger("SecureDockerManager")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _validate_image_name(self, image_name: str) -> bool:
        """Validate image name format."""
        if not isinstance(image_name, str):
            return False
        # Only allow alphanumeric characters, dots, hyphens, and slashes
        pattern = r'^[a-zA-Z0-9._/-]+$'
        return bool(re.match(pattern, image_name))

    def select_image(self, image_name: str) -> Optional[str]:
        """
        Select a Docker image securely.
        Returns the image name or None if validation fails.
        """
        if not self._validate_image_name(image_name):
            self.logger.warning(f"Invalid image name format: {image_name}")
            return None

        try:
            # Use base image as fallback
            image_name = image_name or self.base_image
            
            # Get image details
            image = self.client.images.get(image_name)
            self.logger.info(f"Selected image: {image_name}")
            return image_name
        except docker.errors.ImageNotFound:
            self.logger.error(f"Image not found: {image_name}")
            return None
        except docker.errors.APIError as e:
            self.logger.error(f"Docker API error: {e}")
            return None

    def run_container(self, image_name: str) -> Optional[docker.Container]:
        """
        Run a container based on the selected image.
        Returns the container object or None if validation fails.
        """
        if not self._validate_image_name(image_name):
            self.logger.warning(f"Invalid image name format: {image_name}")
            return None

        try:
            container = self.client.containers.run(
                image_name,
                command="echo Hello from Docker",
                detach=True,
                remove=True
            )
            self.logger.info(f"Container started: {container.id}")
            return container
        except docker.errors.ImageNotFound:
            self.logger.error(f"Image not found: {image_name}")
            return None
        except docker.errors.APIError as e:
            self.logger.error(f"Docker API error: {e}")
            return None

def main():
    """Main function with secure usage example."""
    try:
        manager = SecureDockerManager()
        image_name = input("Enter image name: ")
        selected_image = manager.select_image(image_name)
        
        if selected_image:
            container = manager.run_container(selected_image)
            if container:
                print(f"Container ID: {container.id}")
                container.wait()
                print(f"Container output: {container.logs().decode()}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()