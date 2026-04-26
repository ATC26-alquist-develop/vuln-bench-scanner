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
            raise SystemExit(1)

    def _validate_image_name(self, image_name: str) -> bool:
        """Validate image name format."""
        if not isinstance(image_name, str):
            return False
        # Only allow valid docker image names
        pattern = r'^[a-zA-Z0-9._-]+(/[a-zA-Z0-9._-]+)*:[a-zA-Z0-9._-]+$'
        return bool(re.match(pattern, image_name))

    def select_image(self, image_name: str) -> Optional[str]:
        """
        Securely select a Docker image.
        
        Args:
            image_name: Name of the Docker image to select
            
        Returns:
            Selected image name or None if validation fails
        """
        if not self._validate_image_name(image_name):
            logger.warning(f"Invalid image name format: {image_name}")
            return None
            
        try:
            # Get image details
            image = self.client.images.get(image_name)
            logger.info(f"Selected image: {image_name}")
            return image_name
        except docker.errors.ImageNotFound:
            logger.error(f"Image not found: {image_name}")
            return None
        except docker.errors.APIError as e:
            logger.error(f"Docker API error: {e}")
            return None

    def run_container(self, image_name: str, command: str) -> Optional[str]:
        """
        Securely run a container with the given image and command.
        
        Args:
            image_name: Name of the Docker image
            command: Command to run in the container
            
        Returns:
            Container output or None if execution fails
        """
        if not self._validate_image_name(image_name):
            logger.warning(f"Invalid image name format: {image_name}")
            return None
            
        if not isinstance(command, str) or ';' in command or '&' in command:
            logger.warning("Invalid command format")
            return None

        try:
            # Run container with security options
            container = self.client.containers.run(
                image_name,
                command,
                remove=True,
                detach=True,
                network_mode='none',
                read_only=True,
                cpu_quota=100000,
                mem_limit='512m'
            )
            output = container.decode()
            logger.info(f"Container executed successfully: {image_name}")
            return output
        except docker.errors.APIError as e:
            logger.error(f"Container execution failed: {e}")
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
        print("Invalid image selection")

if __name__ == "__main__":
    main()