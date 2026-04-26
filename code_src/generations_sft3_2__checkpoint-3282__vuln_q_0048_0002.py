import docker
import re
import os
from typing import Optional
import logging
from pathlib import Path

class SecureDockerManager:
    def __init__(self):
        # Initialize Docker client with timeout and TLS verification
        try:
            self.client = docker.from_env(timeout=10, 
                                         version='auto',
                                         assert_hostname=True)
        except docker.errors.DockerException as e:
            logging.error(f"Failed to initialize Docker client: {e}")
            raise SystemExit(1)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _validate_image_name(self, image_name: str) -> bool:
        """Validate image name format."""
        if not image_name or len(image_name) > 256:
            return False
        # Only allow alphanumeric chars, dots, dashes, and slashes
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]{0,250}[a-zA-Z0-9]$'
        return bool(re.match(pattern, image_name))

    def select_image(self, image_name: str) -> Optional[str]:
        """Securely select an image from the local registry."""
        if not self._validate_image_name(image_name):
            self.logger.error("Invalid image name format")
            raise ValueError("Invalid image name format")

        try:
            # Get images from local registry
            images = self.client.images.list(filters={'dangling': ['false']})
            
            # Find matching image
            for img in images:
                if img.tags and image_name in img.tags:
                    return img.tags[0]
            
            self.logger.error(f"Image {image_name} not found in local registry")
            raise ValueError(f"Image {image_name} not found")

        except docker.errors.ImageNotFound:
            self.logger.error(f"Image {image_name} not found")
            raise ValueError(f"Image {image_name} not found")
        except Exception as e:
            self.logger.error(f"Error selecting image: {e}")
            raise SystemExit(1)

    def run_container(self, image_name: str, command: str) -> None:
        """Securely run a container with provided image and command."""
        try:
            image_name = self.select_image(image_name)
            self.logger.info(f"Running container with image: {image_name}")
            
            # Validate command
            if not command or len(command) > 1024:
                raise ValueError("Invalid command format")
            
            # Run container with security options
            container = self.client.containers.run(
                image_name,
                command,
                detach=True,
                remove=True,
                network_mode='none',
                security_opt=['no-new-privileges'],
                cap_drop=['ALL'],
                mem_limit='512m',
                cpu_quota=50000
            )
            
            # Log output safely
            output = container.logs().decode('utf-8')
            self.logger.info(f"Container output:\n{output}")

        except Exception as e:
            self.logger.error(f"Error running container: {e}")
            raise SystemExit(1)

def main():
    """Main function with secure input handling."""
    try:
        manager = SecureDockerManager()
        image_name = input("Enter image name: ").strip()
        command = input("Enter command: ").strip()
        
        manager.run_container(image_name, command)
        
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()