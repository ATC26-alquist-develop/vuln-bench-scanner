import subprocess
from typing import Optional, Tuple

def execute_command(command: list[str], timeout: int = 30) -> Tuple[Optional[str], Optional[str]]:
    """
    Securely execute a system command and return its output.
    
    Args:
        command: List of command arguments (no shell=True)
        timeout: Maximum execution time in seconds
    
    Returns:
        Tuple of (stdout, stderr) as strings or (None, None) if error occurs
    """
    try:
        # Use subprocess.run with security-focused parameters
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=timeout,  # Prevent hanging
            check=True  # Raise CalledProcessError on non-zero exit
        )
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return None, "Command timed out"
    except subprocess.CalledProcessError as e:
        return None, f"Command failed with exit code {e.returncode}"
    except Exception:
        return None, "An error occurred"