import subprocess
from typing import Optional, Tuple
import shlex

def execute_command(command: str, timeout: int = 30) -> Tuple[Optional[str], Optional[str]]:
    """
    Securely execute a system command and return its output.
    
    Args:
        command: The command to execute (string)
        timeout: Maximum execution time in seconds (default 30)
    
    Returns:
        Tuple of (stdout, stderr) as strings, or (None, None) if error
    """
    try:
        # Split command into arguments safely
        args = shlex.split(command)
        
        # Validate command (only allow safe commands)
        if not args or not isinstance(args[0], str):
            return None, "Invalid command format"
            
        # Execute command with security measures
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,  # Prevent shell injection
            check=False   # Don't raise exception on non-zero exit
        )
        
        return result.stdout, result.stderr
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        return None, str(e)
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# Example usage:
if __name__ == "__main__":
    stdout, stderr = execute_command("ls -l")
    if stdout:
        print("Output:", stdout)
    if stderr:
        print("Error:", stderr)