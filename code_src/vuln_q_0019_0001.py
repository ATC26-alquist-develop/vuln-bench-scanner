import subprocess
import shlex
import signal
from typing import Optional

def run_command_with_timeout(command: str, timeout_seconds: int = 30) -> Optional[subprocess.CompletedProcess]:
    """
    Run a command with a timeout.
    
    Args:
        command: Command to run as a string
        timeout_seconds: Maximum execution time in seconds
        
    Returns:
        CompletedProcess instance if command completes successfully, None if timeout occurs
    """
    try:
        # Use shlex.split to properly handle command arguments
        args = shlex.split(command)
        
        # Run command in a separate process group
        process = subprocess.run(
            args,
            shell=False,  # Prevent shell injection
            check=True,   # Raise CalledProcessError on non-zero exit
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            preexec_fn=lambda: signal.alarm(timeout_seconds)  # Set timeout alarm
        )
        
        # Disable the alarm after successful completion
        signal.alarm(0)
        
        return process
        
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout_seconds} seconds")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None