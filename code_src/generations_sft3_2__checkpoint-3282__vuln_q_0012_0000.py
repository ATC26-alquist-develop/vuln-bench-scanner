import subprocess
from typing import Tuple
import os

def run_command(command: list[str], timeout: int = 30) -> Tuple[str, str, int]:
    """
    Securely run an external command and capture its output.
    
    Args:
        command: List of command arguments (first item is the program)
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr, return_code)
        
    Raises:
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: If command fails to execute
    """
    try:
        # Run command with security measures:
        # - shell=False to prevent shell injection
        # - timeout to prevent hanging
        # - capture_output=True to capture stdout/stderr
        # - text=True for string output instead of bytes
        result = subprocess.run(
            command,
            shell=False,
            timeout=timeout,
            capture_output=True,
            text=True
        )
        
        return result.stdout, result.stderr, result.returncode

    except subprocess.TimeoutExpired as e:
        return '', f'Command timed out after {timeout} seconds', 1
    except subprocess.SubprocessError as e:
        return '', f'Command failed: {str(e)}', 1
    except Exception as e:
        return '', f'Unexpected error: {str(e)}', 1

# Example usage:
if __name__ == '__main__':
    # Example: Run ls command
    try:
        stdout, stderr, code = run_command(['ls', '-l'])
        print(f'Output:\n{stdout}')
        print(f'Errors:\n{stderr}')
        print(f'Return code: {code}')
    except Exception as e:
        print(f'Error: {str(e)}')