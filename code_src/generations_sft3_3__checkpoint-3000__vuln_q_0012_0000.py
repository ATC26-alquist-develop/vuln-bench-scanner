import subprocess
from typing import Tuple
import os

def run_command(command: list[str], timeout: int = 30) -> Tuple[str, str, int]:
    """
    Securely run an external command and capture its output.
    
    Args:
        command: List of command arguments (first item is the program)
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr, return_code)
        
    Raises:
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: If command fails to execute
        ValueError: If command is empty
    """
    if not command or not isinstance(command, list):
        raise ValueError("Command must be a non-empty list")
        
    try:
        # Run command with security measures:
        # - shell=False to prevent shell injection
        # - timeout to prevent hanging
        # - capture_output=True to capture stdout/stderr
        # - text=True for string output
        result = subprocess.run(
            command,
            shell=False,
            timeout=timeout,
            capture_output=True,
            text=True
        )
        
        return result.stdout, result.stderr, result.returncode
        
    except subprocess.TimeoutExpired as e:
        raise subprocess.TimeoutExpired(
            cmd=command,
            timeout=timeout,
            output=e.output,
            stderr=e.stderr
        )
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(f"Command failed: {str(e)}")