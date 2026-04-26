import subprocess
import time
import os

def run_command_with_timeout(command: list[str], timeout: int) -> tuple[str, str]:
    """
    Runs a command and terminates it if it doesn't finish within the specified timeout.
    
    Args:
        command: List of command arguments
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr) as strings
        
    Raises:
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: If command fails to execute
    """
    try:
        # Run command with timeout
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,  # Prevent shell injection
            check=True
        )
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired as e:
        # Terminate process if it exceeds timeout
        try:
            os.kill(e.process.pid, 9)  # Send SIGKILL
        except ProcessLookupError:
            pass  # Process already terminated
        raise