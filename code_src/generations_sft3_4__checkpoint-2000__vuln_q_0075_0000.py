import subprocess
import shlex

def execute_command(command: str) -> tuple:
    """
    Safely execute a system command using subprocess.
    
    Args:
        command: Command to execute as a string
        
    Returns:
        tuple: (return_code, stdout, stderr)
        
    Raises:
        ValueError: If command is empty or contains shell metacharacters
    """
    if not command or not isinstance(command, str):
        raise ValueError("Command must be a non-empty string")
        
    # Split command into arguments safely
    try:
        cmd_args = shlex.split(command)
    except ValueError as e:
        raise ValueError(f"Invalid command format: {e}")
        
    # Check for potentially dangerous shell metacharacters
    dangerous_chars = set(';&|><$`\\')
    if any(char in dangerous_chars for char in command):
        raise ValueError("Command contains potentially dangerous characters")
        
    try:
        # Execute command safely without shell
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            shell=False,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Command execution failed: {e}")