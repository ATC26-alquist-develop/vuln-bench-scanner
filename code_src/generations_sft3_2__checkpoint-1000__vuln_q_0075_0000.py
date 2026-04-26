import subprocess
from typing import List, Optional
import shlex

def execute_command(command: List[str], timeout: int = 30) -> Optional[str]:
    """
    Securely execute a system command using subprocess.
    
    Args:
        command: List of command arguments (first item is the command)
        timeout: Maximum execution time in seconds
        
    Returns:
        Command output as string or None if execution fails
    """
    try:
        # Use subprocess.run with shell=False for security
        result = subprocess.run(
            command,
            shell=False,  # Prevent shell injection
            check=True,   # Raise exception on error
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout
        
    except subprocess.TimeoutExpired:
        return None
    except subprocess.CalledProcessError as e:
        return None
    except Exception:
        return None