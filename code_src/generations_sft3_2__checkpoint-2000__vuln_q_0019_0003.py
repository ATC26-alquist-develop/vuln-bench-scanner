import subprocess
import time
import os

def run_command_with_timeout(command: list[str], timeout_seconds: int) -> tuple[str, str, int]:
    """
    Runs a command and terminates it if it doesn't finish within the specified timeout.
    
    Args:
        command: List of command arguments (first item is the command)
        timeout_seconds: Maximum execution time in seconds
    
    Returns:
        Tuple containing (stdout, stderr, return_code)
    
    Raises:
        subprocess.TimeoutExpired: If command execution exceeds timeout
        subprocess.SubprocessError: If command execution fails
    """
    if not isinstance(command, list) or not command:
        raise ValueError("Command must be a non-empty list")
    
    if not isinstance(timeout_seconds, int) or timeout_seconds <= 0:
        raise ValueError("Timeout must be a positive integer")
    
    try:
        # Run command with timeout
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            shell=False,  # Prevent shell injection
            check=True
        )
        
        return result.stdout, result.stderr, result.returncode
        
    except subprocess.TimeoutExpired as e:
        # Terminate the process
        try:
            os.kill(e.pid, 9)  # Send SIGKILL
        except ProcessLookupError:
            pass  # Process already terminated
        
        raise