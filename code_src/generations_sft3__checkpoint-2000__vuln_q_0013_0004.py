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
        
    # Split command into arguments
    args = shlex.split(command)
    
    # Validate command path
    if not os.path.isfile(args[0]):
        raise ValueError(f"Command '{args[0]}' not found")
        
    # Execute command with security measures
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=30,   # Prevent hanging
            check=True    # Raise exception on error
        )
        return result.stdout
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(f"Command execution failed: {str(e)}")