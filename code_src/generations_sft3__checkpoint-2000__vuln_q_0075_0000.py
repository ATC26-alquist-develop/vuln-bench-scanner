import subprocess
import shlex

def execute_command(command: str) -> tuple:
    """
    Safely execute a system command and return its output.
    
    Args:
        command: The command to execute as a string
        
    Returns:
        tuple: (return_code, stdout, stderr)
        
    Raises:
        ValueError: If the command is empty or contains shell metacharacters
    """
    if not command or not isinstance(command, str):
        raise ValueError("Command must be a non-empty string")
        
    # Split the command into arguments safely
    cmd_args = shlex.split(command)
    
    # Check for potentially dangerous characters
    dangerous_chars = set(';&|><$`\\')
    if any(char in dangerous_chars for char in command):
        raise ValueError("Command contains potentially dangerous characters")
    
    try:
        # Execute command safely without shell
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Command execution failed: {str(e)}")