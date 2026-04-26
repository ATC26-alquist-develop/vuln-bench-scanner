import subprocess
from typing import Optional, Tuple
import shlex

def execute_command(command: str, timeout: int = 30) -> Tuple[Optional[str], Optional[str]]:
    """
    Securely execute a system command and return its output.
    
    Args:
        command: The command to execute as a string
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr) as strings, or (None, None) if error occurs
    """
    try:
        # Split command into arguments safely
        cmd_args = shlex.split(command)
        
        # Validate command - only allow specific commands
        allowed_commands = {'ls', 'echo', 'pwd'}  # Add other allowed commands here
        if cmd_args[0] not in allowed_commands:
            return None, "Command not allowed"
            
        # Execute command securely without shell
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            shell=False,
            timeout=timeout,
            check=False
        )
        
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return None, "Command timed out"
    except subprocess.SubprocessError:
        return None, "Command execution failed"
    except Exception:
        return None, "Unexpected error occurred"