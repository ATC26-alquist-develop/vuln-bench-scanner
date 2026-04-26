import subprocess
from typing import Tuple
import os

def run_command_safely(command: list[str], timeout: int = 30) -> Tuple[str, str, int]:
    """
    Safely run an external command and capture its output.
    
    Args:
        command: List of command arguments (not shell string)
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr, return_code)
        
    Raises:
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: If command fails
    """
    try:
        # Run command with security measures:
        # - shell=False to prevent shell injection
        # - timeout to prevent hanging
        # - capture_output to capture stdout/stderr
        # - text=True for string output
        result = subprocess.run(
            command,
            shell=False,
            timeout=timeout,
            capture_output=True,
            text=True,
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

# Example usage:
if __name__ == "__main__":
    try:
        # Example command: ls -l
        stdout, stderr, returncode = run_command_safely(["ls", "-l"])
        print(f"Return code: {returncode}")
        print(f"Output:\n{stdout}")
        print(f"Errors:\n{stderr}")
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        print(f"Error running command: {e}")