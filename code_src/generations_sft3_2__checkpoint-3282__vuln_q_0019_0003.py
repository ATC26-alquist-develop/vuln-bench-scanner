import subprocess
import time
from typing import Optional

def run_command_with_timeout(command: list[str], timeout_seconds: int) -> Optional[str]:
    """
    Runs a command and terminates it if it doesn't finish within the specified time limit.
    
    Args:
        command: List of command arguments (first item is the command)
        timeout_seconds: Maximum execution time in seconds
        
    Returns:
        Command output as string if successful, None if timeout occurs
        
    Raises:
        subprocess.SubprocessError: If command execution fails
    """
    try:
        # Run command with timeout
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        return result.stdout
        
    except subprocess.TimeoutExpired:
        # Command timed out, terminate it
        if 'result' in locals():  # If command was already started
            result.kill()
        raise
    except Exception as e:
        # Handle other subprocess errors
        raise subprocess.SubprocessError(f"Command execution failed: {str(e)}")