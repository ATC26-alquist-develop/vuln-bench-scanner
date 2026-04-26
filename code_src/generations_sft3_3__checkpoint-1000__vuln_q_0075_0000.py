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
        # Use subprocess.run with security-focused parameters
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,  # Don't raise exception on non-zero exit
            shell=False,  # Prevent shell injection
            check=False,  # Don't raise exception on non-zero exit
            # Explicitly set environment variables
            env={
                'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
                'LANG': 'C.UTF-8',
                'LC_ALL': 'C.UTF-8'
            }
        )
        
        return result.stdout
        
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None