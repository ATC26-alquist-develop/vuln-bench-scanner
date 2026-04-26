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
        
    # Whitelist of allowed commands - adjust based on your needs
    allowed_commands = {'ls', 'echo', 'pwd'}
    
    # Split command into parts
    try:
        cmd_parts = shlex.split(command)
    except ValueError as e:
        raise ValueError(f"Invalid command format: {str(e)}")
        
    # Check if base command is allowed
    if cmd_parts[0] not in allowed_commands:
        raise ValueError(f"Command '{cmd_parts[0]}' is not allowed")
        
    # Validate command arguments
    if len(cmd_parts) > 3:  # Limit number of arguments
        raise ValueError("Too many arguments")
        
    # Additional validation of command arguments
    for arg in cmd_parts[1:]:
        if not re.match(r'^[a-zA-Z0-9_\-./]+$', arg):
            raise ValueError("Invalid characters in command arguments")
            
    try:
        # Execute command safely
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            check=True,
            shell=False  # Never use shell=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output
        )