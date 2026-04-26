```python
import docker
import re
import logging
from typing import Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureDockerExecutor:
    def __init__(self, base_image: str = "library/alpine"):
        """Initialize with a default base image."""
        try:
            self.client = docker.from_env()
            self.base_image = base_image
        except docker.errors.DockerException as e:
            logger.error(f"Docker client initialization failed: {e}")
            raise

    def _validate_image_name(self, image_name: str) -> bool:
        """Validate Docker image name format."""
        if not isinstance(image_name, str):
            return False
        # Only allow alphanumeric chars, dash, underscore, and colon
        pattern = r'^[a-zA-Z0-9\-_]+(:[a-zA-Z0-9\-_]+)?$'
        return bool(re.match(pattern, image_name))

    def _sanitize_path(self, path: str) -> Optional[Path]:
        """Sanitize and validate file path."""
        try:
            # Convert to absolute path and resolve any symlinks
            abs_path = Path(path).resolve()
            # Ensure path is within current working directory
            if not str(abs_path).startswith(str(Path.cwd())):
                logger.warning("Attempted to access file outside current directory")
                return None
            return abs_path
        except Exception as e:
            logger.error(f"Path validation failed: {e}")
            return None

    def select_image(self, image_name: str) -> Optional[str]:
        """Securely select a Docker image."""
        if not self._validate_image_name(image_name):
            logger.error("Invalid image name format")
            return None

        try:
            # Get base image
            base = self.client.images.get(self.base_image)
            
            # Try to pull the requested image
            image = self.client.images.pull(image_name)
            
            # Verify image exists
            if image.id != base.id:
                logger.info(f"Selected image: {image_name}")
                return image_name
            else:
                logger.warning("Requested image is the same as base image")
                return None

        except docker.errors.ImageNotFound:
            logger.error(f"Requested image not found: {image_name}")
            return None
        except docker.errors.APIError as e:
            logger.error(f"Docker API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

    def run_command(self, image_name: str, command: str) -> Optional[str]:
        """Run a command in the selected image."""
        if not self._validate_image_name(image_name):
            logger.error("Invalid image name format")
            return None

        try:
            # Get the selected image
            image = self.client.images.get(image_name)
            
            # Run the command
            container = self.client.containers.run(
                image,
                command,
                remove=True,
                detach=True,
                remove=True
            )
            
            return container.decode('utf-8')
            
        except docker.errors.ImageNotFound:
            logger.error(f"Requested image not found: {image_name}")
            return None
        except docker.errors.APIError as e:
            logger.error(f"Docker API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

# Example usage
if __name__ == "__main__":
    executor = SecureDockerExecutor()
    
    # Select an image
    image = executor.select_image("python:3.9-slim")
    if image:
        print(f"Selected image: {image}")
        
        # Run a command
        result = executor.run_command(image, "echo Hello, World