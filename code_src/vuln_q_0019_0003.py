import subprocess
import signal
import time
from typing import Optional, Tuple

def run_command_with_timeout(command: list[str], timeout_seconds: int = 30) -> Tuple[Optional[subprocess.CompletedProcess], Optional[float]]:
    """
    Run a command with a timeout and return its result.
    
    Args:
        command: List of command arguments (not a string)
        timeout_seconds: Maximum execution time in seconds
        
    Returns:
        Tuple of (completed process, execution time) or (None, timeout_time) if timeout occurs
    """
    try:
        # Start the process with a timeout
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout_seconds
        )
        return process, time.time() - start_time
    except subprocess.TimeoutExpired:
        return None, time.time() - start_time
    except subprocess.SubprocessError:
        return None, time.time() - start_time