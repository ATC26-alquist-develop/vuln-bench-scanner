import subprocess
from typing import Optional, Tuple

def run_command(command: str, timeout: int = 30) -> Tuple[Optional[str], Optional[str]]:
    """
    Safely run a shell command and return its output.
    
    Args:
        command: The command to run (as a string)
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr) as strings, or (None, None) if command fails
    """
    try:
        # Use subprocess.run with shell=False for security
        result = subprocess.run(
            command.split(),  # Split command into list to prevent shell injection
            capture_output=True,
            text=True,
            shell=False,
            timeout=timeout,
            check=False  # Don't raise exception on non-zero exit
        )
        
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return None, "Command timed out"
    except subprocess.SubprocessError:
        return None, "Command execution failed"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"