import re
import subprocess
import logging
from typing import Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureDockerExecutor:
    # Whitelist of allowed Docker images
    ALLOWED_IMAGES = {
        'python:3.9-slim',
        'python:3.10-slim',
        'python:3.11-slim'
    }
    
    @staticmethod
    def validate_image_name(image_name: str) -> bool:
        """Validate if the image name is in the whitelist."""
        if not image_name or not isinstance(image_name, str):
            return False
        return image_name in SecureDockerExecutor.ALLOWED_IMAGES

    @staticmethod
    def validate_command(command: str) -> bool:
        """Validate if the command is safe to execute."""
        # Only allow specific safe commands
        safe_commands = {'run', 'ps', 'images', 'version'}
        return command in safe_commands

    @staticmethod
    def execute_docker_command(command: str, image: str) -> Optional[str]:
        """Execute a Docker command securely."""
        try:
            # Validate inputs
            if not SecureDockerExecutor.validate_image_name(image):
                logging.error(f"Invalid image name: {image}")
                return None
            
            if not SecureDockerExecutor.validate_command(command):
                logging.error(f"Invalid command: {command}")
                return None

            # Construct command with arguments as list to prevent shell injection
            cmd_list = ['docker', command, image]

            # Execute command securely without shell=True
            result = subprocess.run(
                cmd_list,
                capture_output=True,
                text=True,
                shell=False,
                timeout=5  # Prevent hanging
            )

            # Log the command execution
            logging.info(f"Executed Docker command: {' '.join(cmd_list)}")

            return result.stdout

        except subprocess.TimeoutExpired:
            logging.error(f"Command timed out: {' '.join(cmd_list)}")
            return None
        except subprocess.SubprocessError as e:
            logging.error(f"Error executing Docker command: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return None

def main():
    while True:
        image = input("Enter Docker image name (or 'q' to quit): ").strip()
        if image.lower() == 'q':
            break

        command = input("Enter Docker command (run, ps, images, version): ").strip()
        
        # Execute command and get output
        output = SecureDockerExecutor.execute_docker_command(command, image)
        
        if output:
            print(f"Output:\n{output}")

if __name__ == "__main__":
    main()