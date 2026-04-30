import subprocess
from typing import Optional

def execute_command(command: list[str]) -> Optional[str]:
    """
    Securely execute a system command and return its output.
    
    Args:
        command: List of command arguments (e.g. ['ls', '-l'])
        
    Returns:
        Command output as string or None if command fails
        
    Raises:
        ValueError: If command is empty or None
    """
    # Input validation
    if not command or not isinstance(command, list):
        raise ValueError("Command must be a non-empty list")
        
    try:
        # Use subprocess.run with shell=False for security
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False,
            check=False  # Don't raise on non-zero exit
        )
        
        return result.stdout
        
    except subprocess.SubprocessError:
        # Handle command execution errors
        return None