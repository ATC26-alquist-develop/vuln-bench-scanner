import subprocess
from typing import Optional, Tuple

def run_command(command: list[str], timeout: int = 30) -> Tuple[Optional[str], Optional[str]]:
    """
    Securely run a shell command and return its output.
    
    Args:
        command: List of command arguments (no shell=True)
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr) as strings, or (None, None) if command fails
        
    Raises:
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: If command fails
    """
    try:
        # Run command securely without shell=True
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout,  # Prevent hanging
            check=False  # Don't raise on non-zero exit
        )
        
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return None, "Command timed out"
    except subprocess.SubprocessError:
        return None, "Command failed"