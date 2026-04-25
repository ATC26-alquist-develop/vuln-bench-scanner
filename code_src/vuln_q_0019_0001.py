import subprocess
import time
import os
from typing import Optional

def run_command_with_timeout(command: list[str], timeout_seconds: int = 30) -> Optional[str]:
    """
    Run a command with a timeout.
    
    Args:
        command: List of command arguments
        timeout_seconds: Maximum execution time in seconds
        
    Returns:
        Command output if successful, None if timeout or error occurs
    """
    try:
        # Start the command in a new process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,  # Prevent shell injection
            cwd=os.getcwd(),  # Set working directory
            env=os.environ.copy()  # Copy environment variables
        )
        
        # Wait for the command to complete or timeout
        try:
            stdout, stderr = process.communicate(timeout=timeout_seconds)
            if process.returncode != 0:
                return None
            return stdout.decode('utf-8')
        except subprocess.TimeoutExpired:
            process.kill()
            return None
        except Exception:
            return None
            
    except Exception:
        return None

# Example usage:
if __name__ == "__main__":
    command = ["ls", "-l", "/tmp"]
    result = run_command_with_timeout(command)
    if result:
        print("Command output:", result)
    else:
        print("Command timed out or failed")