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
        # Only allow alphanumeric, dash, underscore, and colon
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]$'
        return bool(re.match(pattern, image_name))

    def _validate_container_name(self, container_name: str) -> bool:
        """Validate container name format."""
        # Only allow alphanumeric, dash, underscore, and colon
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]$'
        return bool(re.match(pattern, container_name))

    def run_container(self, image_name: str, container_name: str, 
                     command: Optional[str] = None, 
                     port_mapping: Optional[dict] = None) -> bool:
        """
        Securely run a Docker container with validated inputs.
        
        Args:
            image_name: Docker image name
            container_name: Container name
            command: Optional command to run in container
            port_mapping: Optional port mapping dictionary
        
        Returns:
            bool: True if container started successfully, False otherwise
        """
        try:
            # Validate inputs
            if not self._validate_image_name(image_name):
                self.logger.error(f"Invalid image name format: {image_name}")
                return False
                
            if not self._validate_container_name(container_name):
                self.logger.error(f"Invalid container name format: {container_name}")
                return False

            # Create container with security settings
            container = self.client.containers.run(
                image=image_name,
                name=container_name,
                command=command,
                ports=port_mapping,
                detach=True,
                remove=True,
                network_mode='none',  # Prevent network access
                cap_drop=['ALL'],  # Drop all capabilities
                security_opt=['no-new-privileges'],  # Prevent privilege escalation
                read_only=True,  # Read-only filesystem
                mem_limit='512m',  # Memory limit
                cpu_quota=1000  # CPU quota
            )
            
            self.logger.info(f"Container {container_name} started successfully")
            return True

        except docker.errors.DockerException as e:
            self.logger.error(f"Docker error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False