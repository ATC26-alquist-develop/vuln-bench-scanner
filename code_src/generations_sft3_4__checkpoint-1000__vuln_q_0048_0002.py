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

    def validate_image_name(self, image_name: str) -> bool:
        """Validate Docker image name format."""
        if not image_name or len(image_name) > 255:
            return False
        # Only allow alphanumeric chars, dash, underscore, and colon
        pattern = r'^[a-zA-Z0-9\-_:\./]+$'
        return bool(re.match(pattern, image_name))

    def get_image_info(self, image_name: str) -> Optional[dict]:
        """Safely get image information."""
        if not self.validate_image_name(image_name):
            logger.error("Invalid image name format")
            return None

        try:
            image = self.client.images.get(image_name)
            return {
                'id': image.id,
                'name': image.tags[0] if image.tags else image.short_id,
                'size': image.attrs['Size']
            }
        except docker.errors.ImageNotFound:
            logger.error(f"Image not found: {image_name}")
            return None
        except docker.errors.DockerException as e:
            logger.error(f"Error getting image info: {e}")
            return None

    def list_images(self) -> list:
        """List all available images."""
        try:
            return [img.tags[0] if img.tags else img.short_id for img in self.client.images.list()]
        except docker.errors.DockerException as e:
            logger.error(f"Error listing images: {e}")
            return []

    def run_command(self, command: str) -> Optional[str]:
        """Run a Docker command."""
        if not command or len(command) > 2048:
            logger.error("Invalid command length")
            return None

        try:
            # Split command into parts
            parts = command.split()
            if not parts:
                logger.error("Empty command")
                return None

            # Validate first part (command)
            if parts[0] not in ['ps', 'images', 'ps', 'run', 'inspect']:
                logger.error("Invalid command")
                return None

            # Execute command
            if parts[0] == 'ps':
                return self.client.containers.list(all=True)
            elif parts[0] == 'images':
                return self.list_images()
            elif parts[0] == 'run':
                return self.client.containers.run(
                    self.base_image,
                    command=' '.join(parts[1:]),
                    remove=True,
                    remove_output=True
                )
            elif parts[0] == 'inspect':
                return self.client.images.get(parts[1]).attrs
            else:
                logger.error("Unknown command")
                return None

        except docker.errors.DockerException as e:
            logger.error(f"Error executing command: {e}")
            return None

def main():
    """Main function with secure usage example."""
    try:
        executor = SecureDockerExecutor()
        
        # Example usage
        image_info = executor.get_image_info("alpine")
        if image_info:
            print(f"Image info: {image_info}")
        
        commands = [
            "ps",
            "images",
            "run alpine echo 'Hello, World!'",
            "inspect alpine"
        ]
        
        for cmd in commands:
            result = executor.run_command(cmd)
            if result:
                print(f