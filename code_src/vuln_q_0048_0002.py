import docker
import re
from typing import Optional
import logging
from pathlib import Path

class SecureDockerExecutor:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize Docker client
        try:
            self.client = docker.from_env()
        except docker.errors.DockerException as e:
            self.logger.error(f"Failed to initialize Docker client: {e}")
            raise

    def _validate_image_name(self, image_name: str) -> bool:
        """Validate Docker image name format."""
        # Only allow alphanumeric, dash, dot, and underscore
        pattern = r'^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+(:[a-zA-Z0-9._-]+)?$'
        return bool(re.match(pattern, image_name))

    def _validate_command(self, command: str) -> bool:
        """Validate Docker command."""
        # Only allow basic Docker commands
        allowed_commands = {'run', 'ps', 'inspect', 'images', 'version'}
        return command.split()[0] in allowed_commands

    def execute_docker_command(self, image_name: str, command: str) -> Optional[str]:
        """
        Execute a Docker command securely.
        
        Args:
            image_name: Docker image name
            command: Docker command to execute
            
        Returns:
            Command output or None if validation fails
        """
        try:
            # Validate inputs
            if not self._validate_image_name(image_name):
                self.logger.error(f"Invalid image name format: {image_name}")
                return None
                
            if not self._validate_command(command):
                self.logger.error(f"Invalid command: {command}")
                return None

            # Execute command
            result = self.client.containers.run(
                image=image_name,
                command=command,
                remove=True,  # Automatically remove container
                detach=True,  # Run in background
                network_mode='none'  # Isolate container
            )
            
            return result.decode('utf-8')
            
        except docker.errors.APIError as e:
            self.logger.error(f"Docker API error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None

def main():
    executor = SecureDockerExecutor()
    
    while True:
        image_name = input("Enter Docker image name (or 'quit' to exit): ").strip()
        if image_name.lower() == 'quit':
            break
            
        command = input("Enter Docker command: ").strip()
        
        result = executor.execute_docker_command(image_name, command)
        if result:
            print(f"Command output:\n{result}")
        else:
            print("Command execution failed or invalid input.")

if __name__ == "__main__":
    main()