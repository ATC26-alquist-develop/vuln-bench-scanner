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
            self.client = docker.from_env(timeout=30)
        except docker.errors.DockerException as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            raise SystemExit(1)

    def _validate_image_name(self, image_name: str) -> bool:
        """Validate image name format."""
        if not image_name or len(image_name) > 255:
            return False
        # Only allow alphanumeric chars, dots, dashes, and slashes
        pattern = r'^[\w.-]+$'
        return bool(re.match(pattern, image_name))

    def select_image(self, image_name: str) -> Optional[str]:
        """
        Securely select an image from the Docker registry.
        
        Args:
            image_name: Name of the Docker image to select
            
        Returns:
            Selected image name or None if validation fails
        """
        if not self._validate_image_name(image_name):
            logger.warning(f"Invalid image name format: {image_name}")
            return None

        try:
            # Get images with exact match
            images = self.client.images.list(filters={'reference': image_name})
            
            if not images:
                logger.warning(f"No images found matching: {image_name}")
                return None
                
            return images[0].tags[0] if images[0].tags else None
            
        except docker.errors.ImageNotFound:
            logger.warning(f"Image not found: {image_name}")
            return None
        except Exception as e:
            logger.error(f"Error selecting image: {e}")
            return None

    def run_container(self, image_name: str, command: str) -> Optional[str]:
        """
        Securely run a container with the given command.
        
        Args:
            image_name: Name of the Docker image to run
            command: Command to run in the container
            
        Returns:
            Container output or None if execution fails
        """
        if not self._validate_image_name(image_name):
            logger.warning(f"Invalid image name format: {image_name}")
            return None

        try:
            # Validate command
            if not command or len(command) > 1024:
                logger.warning("Invalid command length")
                return None
                
            # Run container with security options
            container = self.client.containers.run(
                image_name,
                command,
                remove=True,
                detach=True,
                network_mode='none',
                read_only=True,
                cpu_quota=50000,
                mem_limit='512m'
            )
            
            return container.decode('utf-8')
            
        except docker.errors.ImageNotFound:
            logger.warning(f"Image not found: {image_name}")
            return None
        except docker.errors.APIError as e:
            logger.error(f"Docker API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error running container: {e}")
            return None

def main():
    executor = SecureDockerExecutor()
    
    # Example usage
    image_name = input("Enter Docker image name: ")
    command = input("Enter command to run: ")
    
    selected_image = executor.select_image(image_name)
    if selected_image:
        result = executor.run_container(selected_image, command)
        if result:
            print(result)
        else:
            print("Container execution failed")
    else:
        print("Image selection failed")

if __name__ == "__main__":
    main()