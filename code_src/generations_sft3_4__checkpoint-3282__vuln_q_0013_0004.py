import subprocess
import shlex
import os

def execute_command(command: str) -> str:
    """
    Execute a command safely using subprocess.
    
    Args:
        command (str): The command to execute
        
    Returns:
        str: Command output
        
    Raises:
        ValueError: If command is empty or contains invalid characters
        subprocess.SubprocessError: If command execution fails
    """
    if not command or not command.strip():
        raise ValueError("Command cannot be empty")
        
    # Whitelist of allowed commands
    allowed_commands = {
        'ls': '/bin/ls',
        'pwd': '/bin/pwd',
        'whoami': '/usr/bin/whoami',
        'date': '/bin/date'
    }
    
    # Split command into parts
    parts = shlex.split(command)
    if not parts:
        raise ValueError("Invalid command format")
        
    # Check if command is in whitelist
    if parts[0] not in allowed_commands:
        raise ValueError(f"Command '{parts[0]}' is not allowed")
        
    # Use full path from whitelist
    command = [allowed_commands[parts[0]]] + parts[1:]
    
    try:
        # Execute command with security measures
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=10,   # Prevent hanging
            check=True    # Raise exception on error
        )
        return result.stdout
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(f"Command execution failed: {str(e)}")