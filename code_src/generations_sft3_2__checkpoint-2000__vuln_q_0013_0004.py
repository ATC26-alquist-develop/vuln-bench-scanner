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
    # Validate input
    if not command or not isinstance(command, str):
        raise ValueError("Command must be a non-empty string")
        
    # Split command into arguments
    args = shlex.split(command)
    
    # Validate command name
    if not args or not args[0]:
        raise ValueError("Invalid command")
        
    # Check if command is in system PATH
    if not os.path.isfile(args[0]):
        raise ValueError(f"Command '{args[0]}' not found in PATH")
        
    try:
        # Execute command with security measures
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