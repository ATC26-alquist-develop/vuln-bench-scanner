```python
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
        ValueError: If command is empty or invalid
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: If command execution fails
    """
    if not command or not isinstance(command, str):
        raise ValueError("Command must be a non-empty string")
        
    try:
        # Use shlex.split to properly handle command arguments
        args = shlex.split(command)
        
        # Run command with security measures
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout,  # Prevent hanging
            check=True  # Raise on non-zero exit
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
        raise subprocess.SubprocessError(
            cmd=e.cmd,
            output=e.output,
            stderr=e.stderr
        )
```