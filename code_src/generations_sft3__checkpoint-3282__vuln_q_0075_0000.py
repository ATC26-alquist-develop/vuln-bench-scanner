import subprocess
import shlex
import re

def execute_command(command: str) -> str:
    """
    Safely execute a system command with input validation.
    
    Args:
        command: The command to execute
        
    Returns:
        str: Command output
        
    Raises:
        ValueError: If command is invalid or contains suspicious characters
        subprocess.CalledProcessError: If command execution fails
    """
    # Input validation
    if not command or not isinstance(command, str):
        raise ValueError("Command must be a non-empty string")
        
    # Only allow alphanumeric characters, spaces, and common symbols
    if not re.match(r'^[a-zA-Z0-9\s\-_./&|()]+$', command):
        raise ValueError("Invalid characters in command")
        
    try:
        # Use subprocess.run with shell=False for security
        result = subprocess.run(
            shlex.split(command),  # Safely split the command
            capture_output=True,
            text=True,
            check=True,
            shell=False  # Crucial security setting
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output
        )