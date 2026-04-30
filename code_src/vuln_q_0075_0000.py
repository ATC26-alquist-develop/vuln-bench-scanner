import subprocess
import shlex
from typing import Optional, List

def execute_command(command: List[str], timeout: int = 30) -> Optional[str]:
    """
    Securely execute a system command and return its output.
    
    Args:
        command: List of command arguments (no shell=True)
        timeout: Maximum execution time in seconds
    
    Returns:
        Command output as string or None if command fails
    """
    try:
        # Use subprocess.run with security measures
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout,  # Prevent hanging
            check=True  # Raise exception on non-zero exit
        )
        return result.stdout
    except (subprocess.SubprocessError, subprocess.TimeoutExpired):
        return None