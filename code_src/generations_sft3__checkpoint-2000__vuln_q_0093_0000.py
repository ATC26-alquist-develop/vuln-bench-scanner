import subprocess
from typing import Optional, Tuple
import shlex

def execute_command(command: str, timeout: int = 30) -> Tuple[Optional[str], Optional[str]]:
    """
    Securely execute a system command and return its output.
    
    Args:
        command: Command to execute as string
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr) as strings, or (None, None) on error
    """
    try:
        # Split command into arguments safely
        cmd_args = shlex.split(command)
        
        # Validate command is not empty
        if not cmd_args:
            return None, "Empty command"
            
        # Execute command securely without shell
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            shell=False,
            timeout=timeout,
            check=False
        )
        
        # Return output safely
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return None, "Command timed out"
    except subprocess.SubprocessError as e:
        return None, f"Subprocess error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"