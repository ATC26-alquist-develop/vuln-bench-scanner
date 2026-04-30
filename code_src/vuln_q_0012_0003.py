```python
import subprocess
import logging
from typing import Tuple
from pathlib import Path

def run_command(command: list[str], timeout: int = 5) -> Tuple[str, str]:
    """
    Securely run a shell command and return its output.
    
    Args:
        command: List of command arguments (not shell string)
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr) as strings
        
    Raises:
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: If command fails to execute
        ValueError: If command is invalid
    """
    # Input validation
    if not command or not isinstance(command, list):
        raise ValueError("Command must be a non-empty list")
    
    # Validate each argument
    for arg in command:
        if not isinstance(arg, str) or not arg.strip():
            raise ValueError("All command arguments must be non-empty strings")
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Run command securely without shell=True
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout,  # Prevent hanging
            check=True  # Raise on non-zero exit
        )
        
        logger.info(f"Command executed successfully: {command}")
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired as e:
        logger.error(f"Command timed out after {timeout} seconds: {command}")
        raise
    except subprocess.SubprocessError as e:
        logger.error(f"Error running command: {command}")
        raise
```