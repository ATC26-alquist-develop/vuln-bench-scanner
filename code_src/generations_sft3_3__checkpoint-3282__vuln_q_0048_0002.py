import docker
import re
import logging
from typing import Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureDockerExecutor:
    def __init__(self):
        # Initialize Docker client with timeout
        try:
            self.client = docker.from_env(timeout=10)
        except docker.errors.DockerException as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            raise

    def _validate_image_name(self, image_name: str) -> bool:
        """Validate image name format."""
        # Only allow alphanumeric chars, dots, dashes, and slashes
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]+[a-zA-Z0-9]+$'
        return bool(re.match(pattern, image_name))

    def _sanitize_path(self, path: str) -> str:
        """Sanitize and validate path."""
        try:
            # Convert to absolute path and resolve any symlinks
            sanitized = str(Path(path).resolve())
            if not Path(sanitized).is_absolute():
                raise ValueError("Path must be absolute")
            return sanitized
        except Exception as e:
            logger.error(f"Path validation failed: {e}")
            raise ValueError("Invalid path")

    def select_image(self, image_name: str) -> Optional[str]:
        """
        Securely select an image from the Docker registry.
        
        Args:
            image_name: Name of the Docker image to select
            
        Returns:
            Optional[str]: Full image tag if successful, None otherwise
        """
        if not isinstance(image_name, str):
            logger.error("Invalid input type")
            return None

        if not self._validate_image_name(image_name):
            logger.error("Invalid image name format")
            return None

        try:
            # Get image details
            image = self.client.images.get(image_name)
            return image.tags[0] if image.tags else None
        except docker.errors.ImageNotFound:
            logger.error(f"Image not found: {image_name}")
            return None
        except Exception as e:
            logger.error(f"Error selecting image: {e}")
            return None

    def run_container(self, image_name: str, container_name: str) -> Optional[str]:
        """
        Securely run a container based on the selected image.
        
        Args:
            image_name: Name of the Docker image to use
            container_name: Name for the container
            
        Returns:
            Optional[str]: Container ID if successful, None otherwise
        """
        if not isinstance(image_name, str) or not isinstance(container_name, str):
            logger.error("Invalid input types")
            return None

        image_name = self.select_image(image_name)
        if not image_name:
            return None

        try:
            # Create and start container with security options
            container = self.client.containers.run(
                image_name,
                name=container_name,
                detach=True,
                remove=True,
                network_mode='none',
                cap_drop=['ALL'],
                security_opt=['no-new-privileges']
            )
            return container.id
        except Exception as e:
            logger.error(f"Error running container: {e}")
            return None

def main():
    executor = SecureDockerExecutor()
    
    # Example usage
    try:
        container_id = executor.run_container("python:3.9-slim", "my_secure_container")
        if container_id:
            logger.info(f"Container started with ID: {container_id}")
        else:
            logger.error("Failed to start container")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()