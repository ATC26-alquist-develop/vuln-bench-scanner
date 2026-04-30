```python
import subprocess
import os
import signal
from typing import Optional

def run_command_with_timeout(command: list[str], timeout_seconds: int = 30) -> Optional[str]:
    """
    Run a command with a timeout.
    
    Args:
        command: List of command arguments (first item is the command, rest are arguments)
        timeout_seconds: Maximum time to wait for command completion
        
    Returns:
        Command output if completed within timeout, None otherwise
    """
    if not command or not isinstance(command, list):
        raise ValueError("Command must be a non-empty list")

    if not isinstance(timeout_seconds, int) or timeout_seconds <= 0:
        raise ValueError("Timeout must be a positive integer")

    try:
        # Start the process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,  # Avoid shell injection vulnerabilities
            text=True,
            # Use a custom function to handle SIGALRM
            preexec_fn=lambda: signal.signal(signal.SIGALRM, _handle_timeout)
        )

        # Set the alarm
        signal.alarm(timeout_seconds)

        # Get the output
        try:
            stdout, stderr = process.communicate(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            # If timeout occurs, terminate the process
            process.kill()
            signal.alarm(0)  # Cancel the alarm
            return None

        # Cancel the alarm if process completed
        signal.alarm(0)

        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode, command[0], output=stdout, stderr=stderr
            )

        return stdout

    except Exception as e:
        # Ensure the alarm is canceled in case of any other errors
        signal.alarm(0)
        raise RuntimeError(f"Failed to run command: {str(e)}")

def _handle_timeout(signum, frame):
    raise TimeoutError("Command execution timed out")

# Example usage
if __name__ == "__main__":
    try:
        # Example: List directory contents with timeout
        result = run_command_with_timeout(["ls", "-l"])
        if result:
            print(result)
        else:
            print("Command timed out")
    except Exception as e:
        print(f"Error: {e}")
```