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
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]+[a-zA-Z0-9]$'
        return bool(re.match(pattern, image_name))

    def _sanitize_path(self, path: str) -> Path:
        """Sanitize and validate file path."""
        try:
            # Convert to absolute path and resolve any symlinks
            safe_path = Path(path).resolve()
            # Ensure path is within current working directory
            if not str(safe_path).startswith(str(Path.cwd())):
                raise ValueError("Path must be within current directory")
            return safe_path
        except Exception as e:
            logger.error(f"Path validation failed: {e}")
            raise

    def select_image(self, image_name: str) -> Optional[str]:
        """
        Securely select a Docker image.
        
        Args:
            image_name: Name of the Docker image to select
            
        Returns:
            Image ID if successful, None if validation fails
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
            return image.id
            
        except docker.errors.ImageNotFound:
            logger.error(f"Image not found: {image_name}")
            return None
        except docker.errors.APIError as e:
            logger.error(f"Docker API error: {e}")
            return None

    def execute_command(self, image_id: str, command: str) -> Optional[str]:
        """
        Execute a Docker command on a specific image.
        
        Args:
            image_id: Docker image ID
            command: Command to execute
            
        Returns:
            Command output if successful, None if execution fails
        """
        if not isinstance(image_id, str) or not isinstance(command, str):
            logger.error("Invalid input types")
            return None

        try:
            # Execute command with timeout
            container = self.client.containers.run(
                image_id,
                command,
                remove=True,
                detach=True,
                timeout=30
            )
            return container.decode('utf-8')
        except docker.errors.APIError as e:
            logger.error(f"Docker command execution failed: {e}")
            return None

def main():
    executor = SecureDockerExecutor()
    
    # Example usage
    try:
        image_id = executor.select_image("python:3.9-slim")
        if image_id:
            output = executor.execute_command(image_id, "echo Hello, World!")
            if output:
                print(output)
    except Exception as e:
        logger.error(f"Operation failed: {e}")

if __name__ == "__main__":
    main()