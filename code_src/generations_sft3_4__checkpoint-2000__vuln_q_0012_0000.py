import subprocess
from typing import Tuple
import shlex

def run_command(command: str, timeout: int = 30) -> Tuple[str, str, int]:
    """
    Securely run an external command and capture its output.
    
    Args:
        command: The command to run as a string
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr, return_code)
        
    Raises:
        subprocess.TimeoutExpired: If command execution exceeds timeout
        subprocess.SubprocessError: If command execution fails
    """
    try:
        # Split command into arguments safely
        cmd_args = shlex.split(command)
        
        # Run command with security measures:
        # - shell=False to prevent shell injection
        # - timeout to prevent hanging
        # - capture_output to capture stdout/stderr
        # - text=True for string output
        result = subprocess.run(
            cmd_args,
            shell=False,
            timeout=timeout,
            capture_output=True,
            text=True,
            check=False  # Don't raise on non-zero exit
        )
        
        return result.stdout, result.stderr, result.returncode
        
    except subprocess.TimeoutExpired as e:
        return "", f"Command timed out after {timeout} seconds", 1
    except subprocess.SubprocessError as e:
        return "", f"Command execution failed: {str(e)}", 1