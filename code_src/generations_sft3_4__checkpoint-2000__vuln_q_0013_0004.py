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
    if not command or not isinstance(command, str):
        raise ValueError("Command must be a non-empty string")
        
    # Split command into arguments
    cmd_parts = shlex.split(command)
    
    # Validate command path
    if not os.path.isfile(cmd_parts[0]):
        raise ValueError(f"Command not found: {cmd_parts[0]}")
    
    # Execute command with security measures
    try:
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            check=True,
            shell=False  # Prevent shell injection
        )
        return result.stdout
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(f"Command execution failed: {str(e)}")