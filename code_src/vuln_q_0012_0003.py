import subprocess
from typing import Optional, Tuple
import shlex

def run_command(command: str, timeout: int = 30) -> Tuple[Optional[str], Optional[str]]:
    """
    Safely run a shell command and return its output.
    
    Args:
        command: The command to run (as a string)
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr) as strings, or (None, error_message) if command fails
    """
    try:
        # Use shlex.split to properly handle command arguments
        args = shlex.split(command)
        
        # Run command with security measures
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout,  # Prevent hanging
            check=True  # Raise CalledProcessError on non-zero exit
        )
        
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return None, "Command timed out"
    except subprocess.CalledProcessError as e:
        return None, f"Command failed with exit code {e.returncode}: {e.stderr}"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"