import subprocess
import signal
import time
from typing import Optional, Tuple

def run_command_with_timeout(
    command: list[str],
    timeout_seconds: int = 30,
    timeout_message: str = "Command timed out"
) -> Tuple[Optional[subprocess.CompletedProcess], Optional[str]]:
    """
    Run a command with a timeout.
    
    Args:
        command: List of command arguments (not a string)
        timeout_seconds: Maximum execution time in seconds
        timeout_message: Message to display if timeout occurs
        
    Returns:
        Tuple of (process, error_message) where process is None if timeout occurred
    """
    try:
        # Start the process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,  # Security: don't use shell=True
            text=True,
            cwd=None,  # Don't change working directory
            env=None,  # Don't inherit environment variables
            start_new_session=True  # Create new session
        )
        
        # Wait for process to complete or timeout
        try:
            # Set timeout
            timeout = time.time() + timeout_seconds
            
            # Wait for process to complete
            while True:
                # Check if process is still running
                if process.poll() is not None:
                    break
                
                # Check if timeout has been reached
                if time.time() > timeout:
                    process.kill()
                    return None, timeout_message
                
                # Sleep for a short time to prevent busy-waiting
                time.sleep(0.1)
                
            # Process completed successfully
            stdout, stderr = process.communicate()
            return process, None
            
        except Exception as e:
            # Handle unexpected errors
            return None, f"Error: {str(e)}"
            
    except Exception as e:
        # Handle errors during process creation
        return None, f"Error creating process: {str(e)}"