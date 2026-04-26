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
        if not isinstance(image_name, str):
            return False
        # Only allow valid docker image names
        pattern = r'^[a-zA-Z0-9._-]+(/[a-zA-Z0-9._-]+)*:[a-zA-Z0-9._-]+$'
        return bool(re.match(pattern, image_name))

    def _sanitize_path(self, path: str) -> str:
        """Sanitize and validate file path."""
        try:
            # Convert to absolute path and resolve any symlinks
            abs_path = str(Path(path).resolve())
            # Ensure path exists and is a directory
            Path(abs_path).mkdir(parents=True, exist_ok=True)
            return abs_path
        except (OSError, RuntimeError) as e:
            logger.error(f"Path validation failed: {e}")
            raise SystemExit(1)

    def select_image(self, image_name: str) -> Optional[str]:
        """Securely select and return an image."""
        if not self._validate_image_name(image_name):
            logger.error("Invalid image name format")
            raise ValueError("Invalid image name format")

        try:
            # Get image by name
            image = self.client.images.get(image_name)
            logger.info(f"Selected image: {image_name}")
            return image.id
        except docker.errors.ImageNotFound:
            logger.error(f"Image not found: {image_name}")
            raise SystemExit(1)
        except docker.errors.APIError as e:
            logger.error(f"Docker API error: {e}")
            raise SystemExit(1)

    def run_container(self, image_id: str, command: str) -> None:
        """Securely run a container with provided image and command."""
        if not isinstance(image_id, str) or not isinstance(command, str):
            raise ValueError("Invalid input types")

        # Validate command
        allowed_commands = {'ps', 'ls', 'cat', 'echo'}
        if command not in allowed_commands:
            raise ValueError(f"Command not allowed. Allowed commands: {allowed_commands}")

        try:
            container = self.client.containers.run(
                image_id,
                command,
                remove=True,
                detach=False,
                remove=True
            )
            logger.info(f"Container output: {container.decode('utf-8')}")
        except docker.errors.APIError as e:
            logger.error(f"Container execution failed: {e}")
            raise SystemExit(1)

def main():
    """Main execution with input validation."""
    try:
        executor = SecureDockerExecutor()
        
        # Get user input with validation
        image_name = input("Enter Docker image name: ").strip()
        if not executor._validate_image_name(image_name):
            logger.error("Invalid image name format")
            raise ValueError("Invalid image name format")

        # Select and run container
        image_id = executor.select_image(image_name)
        command = input("Enter command to run: ").strip()
        executor.run_container(image_id, command)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()