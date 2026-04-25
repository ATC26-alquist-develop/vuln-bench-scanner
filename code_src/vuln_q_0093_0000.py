import subprocess
from typing import Optional, Tuple

def execute_command(command: str, timeout: int = 30) -> Tuple[Optional[str], Optional[str]]:
    """
    Securely execute a system command and return its output.
    
    Args:
        command: Command to execute as a string
        timeout: Maximum execution time in seconds
    
    Returns:
        Tuple of (stdout, stderr) as strings or (None, None) if error occurs
    """
    try:
        # Use subprocess.run with security-focused parameters
        result = subprocess.run(
            command.split(),  # Split command into list to prevent shell injection
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout,  # Prevent hanging
            check=False  # Don't raise exception on non-zero exit
        )
        
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return None, "Command timed out"
    except subprocess.SubprocessError:
        return None, "Command execution failed"
    except Exception:
        return None, "Unexpected error occurred"