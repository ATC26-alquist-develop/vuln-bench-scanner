import subprocess
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
        # Use subprocess.run with security-focused parameters
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout,  # Prevent hanging
            check=False  # Don't raise exception on non-zero exit
        )
        
        return result.stdout if result.returncode == 0 else None
        
    except subprocess.TimeoutExpired:
        return None
    except subprocess.SubprocessError:
        return None
    except Exception:
        return None