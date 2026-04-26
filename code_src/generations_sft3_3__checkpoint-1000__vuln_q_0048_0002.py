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

    def _validate_path(self, path: str) -> bool:
        """Validate path to ensure it's safe."""
        try:
            path_obj = Path(path)
            return path_obj.exists() and path_obj.is_file()
        except (TypeError, ValueError):
            return False

    def select_image(self, image_name: str) -> Optional[str]:
        """Securely select a Docker image."""
        if not self._validate_image_name(image_name):
            logger.error("Invalid image name format")
            return None

        try:
            # Use base image as fallback
            image = self.base_image if image_name == "" else image_name
            return image
        except Exception as e:
            logger.error(f"Image selection failed: {e}")
            return None

    def run_command(self, command: str) -> Optional[str]:
        """Run a Docker command securely."""
        if not isinstance(command, str):
            logger.error("Invalid command format")
            return None

        try:
            # Split command into parts
            parts = command.split()
            if len(parts) < 2:
                logger.error("Invalid command format")
                return None

            # Execute command with strict validation
            result = self.client.containers.run(
                self.select_image(parts[0]),
                command=parts[1],
                remove=True,
                remove_output=True,
                timeout=30,
                remove=True
            )
            return result
        except docker.errors.DockerException as e:
            logger.error(f"Docker command execution failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return None

def main():
    """Example usage of SecureDockerExecutor."""
    executor = SecureDockerExecutor()
    
    # Example usage
    try:
        result = executor.run_command("ls -l")
        if result:
            print(result)
    except Exception as e:
        logger.error(f"Main execution failed: {e}")

if __name__ == "__main__":
    main()