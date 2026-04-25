import subprocess
from typing import Optional, List
import shlex

def execute_command(command: str, timeout: int = 30) -> Optional[str]:
    """
    Securely execute a system command and return its output.
    
    Args:
        command: Command to execute (string)
        timeout: Maximum execution time in seconds (default 30)
    
    Returns:
        Command output as string or None if execution fails
    """
    try:
        # Use subprocess.run with security measures
        result = subprocess.run(
            shlex.split(command),  # Safely split command string
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout,  # Prevent hanging
            check=False  # Don't raise exception on non-zero exit
        )
        
        return result.stdout if result.stdout else None
        
    except (subprocess.SubprocessError, subprocess.TimeoutExpired, 
            ValueError, OSError) as e:
        # Log error here if needed
        return None