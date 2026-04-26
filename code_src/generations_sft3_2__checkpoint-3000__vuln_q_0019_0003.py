import subprocess
import time
from typing import Optional

def run_command_with_timeout(command: list[str], timeout_seconds: int) -> Optional[str]:
    """
    Runs a command and terminates it if it doesn't finish within the specified timeout.
    
    Args:
        command: List of command arguments
        timeout_seconds: Maximum execution time in seconds
        
    Returns:
        Command output as string if successful, None if timeout occurs
        
    Raises:
        subprocess.TimeoutExpired: If command execution exceeds timeout
        subprocess.SubprocessError: If command execution fails
    """
    try:
        # Run command with timeout
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=True
        )
        return result.stdout
    except subprocess.TimeoutExpired as e:
        print(f"Command timed out after {timeout_seconds} seconds")
        return None
    except subprocess.SubprocessError as e:
        print(f"Command execution failed: {e}")
        return None