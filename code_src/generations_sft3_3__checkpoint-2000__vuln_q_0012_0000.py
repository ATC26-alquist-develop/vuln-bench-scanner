import subprocess
from typing import Tuple
import os

def run_command(command: list[str], timeout: int = 30) -> Tuple[str, str, int]:
    """
    Securely run an external command and capture its output.
    
    Args:
        command: List of command arguments (not shell string)
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr, return_code)
        
    Raises:
        subprocess.TimeoutExpired: If command execution exceeds timeout
        subprocess.SubprocessError: If command execution fails
    """
    try:
        # Run command with security measures:
        # - shell=False to prevent shell injection
        # - timeout to prevent hanging
        # - capture_output=True to capture output
        # - text=True for string output
        result = subprocess.run(
            command,
            shell=False,
            timeout=timeout,
            capture_output=True,
            text=True
        )
        
        return result.stdout, result.stderr, result.returncode

    except subprocess.TimeoutExpired as e:
        return '', f'Timeout after {timeout} seconds', 1
    except subprocess.SubprocessError as e:
        return '', f'Command failed: {str(e)}', 1

# Example usage:
if __name__ == '__main__':
    # Example: Run 'ls' command
    try:
        stdout, stderr, code = run_command(['ls', '-l'])
        if code == 0:
            print(f"Output:\n{stdout}")
        else:
            print(f"Error:\n{stderr}")
    except Exception as e:
        print(f"Error: {str(e)}")