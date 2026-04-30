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
        subprocess.SubprocessError: For other subprocess errors
    """
    try:
        # Use shlex.split to properly handle command arguments
        args = shlex.split(command)
        
        # Run command in a controlled environment
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout,
            check=False  # Don't raise on non-zero exit
        )
        
        return result.stdout, result.stderr, result.returncode
        
    except subprocess.TimeoutExpired as e:
        raise subprocess.TimeoutExpired(
            cmd=e.cmd,
            timeout=e.timeout,
            output=e.output,
            stderr=e.stderr
        )
    except subprocess.SubprocessError as e:
        raise