import subprocess
from typing import Tuple
import shlex

def run_command_safely(command: str, timeout: int = 30) -> Tuple[str, str, int]:
    """
    Safely run an external command and capture its output.
    
    Args:
        command: Command to run as a string
        timeout: Maximum execution time in seconds
    
    Returns:
        Tuple of (stdout, stderr, return_code)
    
    Raises:
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: If command fails to execute
        ValueError: If command is empty or invalid
    """
    # Validate input
    if not command or not isinstance(command, str):
        raise ValueError("Command must be a non-empty string")
    
    # Use shlex.split to properly handle command arguments
    try:
        args = shlex.split(command)
    except ValueError:
        raise ValueError("Invalid command format")
    
    # Run command with security measures
    try:
        # Run command with shell=False for security
        # Capture output and error
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,
            timeout=timeout,
            check=False  # Don't raise on non-zero exit
        )
        return result.stdout, result.stderr, result.returncode
        
    except subprocess.TimeoutExpired as e:
        raise subprocess.TimeoutExpired(
            cmd=e.cmd,
            timeout=timeout,
            output=e.output,
            stderr=e.stderr
        )
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(
            cmd=e.cmd,
            output=e.output,
            stderr=e.stderr
        )