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
    
    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            shell=False  # Prevent shell injection
        )
        if time.time() - start_time > timeout_seconds:
            raise subprocess.TimeoutExpired(
                cmd=command,
                timeout=timeout_seconds,
                output=result.stdout,
                stderr=result.stderr
            )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as e:
        if os.name == 'nt':  # Windows
            raise subprocess.TimeoutExpired(
                cmd=e.cmd,
                timeout=e.timeout,
                output=e.output,
                stderr=e.stderr
            ) from e
        else:  # Unix-like systems
            raise subprocess.TimeoutExpired(
                cmd=e.cmd,
                timeout=e.timeout,
                output=e.stdout,
                stderr=e.stderr
            ) from e