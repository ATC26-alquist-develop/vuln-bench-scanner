import docker
import re
import logging
from typing import Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureDockerExecutor:
    def __init__(self, allowed_images: set[str]):
        """Initialize with a set of allowed images."""
        self.allowed_images = allowed_images
        
    def _validate_image_name(self, image_name: str) -> bool:
        """Validate image name format."""
        # Only allow alphanumeric characters, dots, dashes, and colons
        pattern = r'^[a-zA-Z0-9._-]+(?:/[a-zA-Z0-9._-]+)*$'
        return bool(re.match(pattern, image_name))
    
    def _validate_image_path(self, image_path: str) -> bool:
        """Validate image path."""
        try:
            path = Path(image_path)
            return path.exists() and path.is_file()
        except (TypeError, ValueError):
            return False
    
    def select_image(self, image_name: str) -> Optional[str]:
        """Safely select an image from the allowed list."""
        if not self._validate_image_name(image_name):
            logger.error(f"Invalid image name format: {image_name}")
            return None
            
        if image_name in self.allowed_images:
            return image_name
        else:
            logger.warning(f"Image not in allowed list: {image_name}")
            return None
    
    def run_docker_command(self, image_name: str, command: str) -> Optional[str]:
        """Execute a Docker command with strict validation."""
        if not image_name:
            logger.error("No image specified")
            return None
            
        try:
            # Initialize Docker client
            client = docker.from_env()
            
            # Validate image path if it's a local path
            if self._validate_image_path(image_name):
                image = client.images.get(image_name)
            else:
                image = client.images.get_by_name(image_name)
                
            if not image:
                logger.error(f"Image not found: {image_name}")
                return None
                
            # Validate command
            if not command or len(command) > 100:  # Reasonable command length limit
                logger.error("Invalid command")
                return None
                
            # Execute command with timeout
            result = client.containers.run(
                image.id,
                command,
                remove=True,
                timeout=30,
                remove=True
            )
            return result.decode('utf-8')
            
        except docker.errors.ImageNotFound:
            logger.error(f"Image not found: {image_name}")
            return None
        except docker.errors.APIError as e:
            logger.error(f"Docker API error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None
        finally:
            if 'client' in locals():
                client.close()

def main():
    # Initialize with allowed images
    allowed_images = {
        "python:3.9-slim",
        "nginx:latest",
        "alpine:3.11"
    }
    
    executor = SecureDockerExecutor(allowed_images)
    
    while True:
        image_name = input("Enter image name or path: ").strip()
        command = input("Enter command: ").strip()
        
        result = executor.run_docker_command(image_name, command)
        if result is not None:
            print(result)
        else:
            print("Command execution failed")

if __name__ == "__main__":
    main()