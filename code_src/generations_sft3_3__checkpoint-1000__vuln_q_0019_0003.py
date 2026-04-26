import subprocess
import time
import os

def run_command_with_timeout(command: list[str], timeout: int) -> tuple[str, str, int]:
    """
    Runs a command and terminates it if it doesn't finish within the specified timeout.
    
    Args:
        command: List of command arguments
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr, return_code)
        
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
            timeout=timeout,
            check=True
        )
        return result.stdout, result.stderr, result.returncode
        
    except subprocess.TimeoutExpired as e:
        # Terminate the process
        os.kill(e.process.pid, 9)
        raise