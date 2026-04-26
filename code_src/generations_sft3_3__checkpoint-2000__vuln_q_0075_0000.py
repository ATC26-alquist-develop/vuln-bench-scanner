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
        
    # Whitelist of allowed commands
    allowed_commands = {'ls', 'echo', 'pwd'}
    
    # Split command into parts
    parts = shlex.split(command)
    if not parts:
        raise ValueError("Empty command")
        
    # Check if command is in whitelist
    if parts[0] not in allowed_commands:
        raise ValueError(f"Command '{parts[0]}' is not allowed")
        
    try:
        # Execute command safely without shell
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            check=True,
            shell=False
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output
        )