```python
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
```


This implementation addresses several security concerns:

1. Input validation: We validate both the image name and command against whitelists to prevent unauthorized access or execution of potentially dangerous commands.

2. Command execution: We use `subprocess.run` with a list of arguments instead of a shell, preventing shell injection vulnerabilities.

3. Timeout: We set a timeout to prevent potential hanging or resource exhaustion attacks.

4. Error handling: We catch and log various types of errors without exposing sensitive information.

5. Logging: We implement logging for auditing and monitoring purposes.

6. Type hinting: We use type hints to improve code reliability.

7. Least privilege: The code only allows specific, safe Docker commands.

8. No shell=True: We avoid using shell=True in subprocess calls, which is a common security risk.

This implementation provides a secure way to execute Docker commands based on user input while maintaining a high level of security. However, it's important to note that allowing any form of user input to interact with system resources always carries some risk. In a production environment