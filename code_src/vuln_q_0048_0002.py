import docker
import re
from typing import Optional
import logging
from docker.errors import DockerException

class SecureDockerExecutor:
    def __init__(self):
        self.client = docker.from_env()
        self.allowed_images = set()  # Predefined list of allowed images
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def validate_image_name(self, image_name: str) -> bool:
        """Validate image name against strict pattern."""
        pattern = r'^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$'
        return bool(re.match(pattern, image_name))

    def get_allowed_images(self) -> set:
        """Return a set of allowed image names."""
        return self.allowed_images

    def execute_docker_command(self, image_name: str) -> Optional[str]:
        """Execute a Docker command securely."""
        try:
            if not self.validate_image_name(image_name):
                self.logger.error(f"Invalid image name: {image_name}")
                return None

            if image_name not in self.get_allowed_images():
                self.logger.error(f"Image not allowed: {image_name}")
                return None

            container = self.client.containers.run(
                image=image_name,
                command='echo "Hello, World!"',
                remove=True,
                detach=True
            )
            return container.logs().decode('utf-8')

        except DockerException as e:
            self.logger.error(f"Docker error: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return None

# Usage example
if __name__ == "__main__":
    executor = SecureDockerExecutor()
    executor.allowed_images = {"alpine:latest", "python:3.9-slim"}  # Example allowed images
    result = executor.execute_docker_command("alpine:latest")
    if result:
        print(result)