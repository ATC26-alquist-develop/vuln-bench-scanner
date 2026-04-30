import subprocess
import logging
from typing import Optional

def execute_command(command: list[str]) -> Optional[str]:
    """
    Securely execute a system command and return its output.
    
    Args:
        command: List of command arguments (e.g. ['ls', '-l'])
        
    Returns:
        Command output as string, or None if execution fails
    """
    # Input validation
    if not command or not isinstance(command, list):
        logging.error("Invalid command format")
        return None
        
    # Validate each argument
    for arg in command:
        if not isinstance(arg, str) or not arg.strip():
            logging.error("Invalid command argument")
            return None
            
    try:
        # Use subprocess.run with security measures:
        # - shell=False prevents command injection
        # - capture_output captures stdout/stderr
        # - text=True returns string output
        # - check=True raises exception on non-zero exit
        result = subprocess.run(
            command,
            shell=False,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.SubprocessError as e:
        logging.error(f"Command execution failed: {str(e)}")
        return None