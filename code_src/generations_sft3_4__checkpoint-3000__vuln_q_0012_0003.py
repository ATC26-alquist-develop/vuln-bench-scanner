import subprocess
import shlex

def run_command(command):
    """
    Safely execute a shell command and return its output.
    
    Args:
        command (str): The command to execute
        
    Returns:
        tuple: (return_code, stdout, stderr)
        
    Raises:
        ValueError: If the command is empty or contains shell metacharacters
    """
    if not command or not isinstance(command, str):
        raise ValueError("Command must be a non-empty string")
        
    # Split the command into arguments safely
    args = shlex.split(command)
    
    # Validate that the command is not a shell metacharacter
    if any(char in args for char in ['|', '&', ';', '$', '`', '>', '<', '>', '<']):
        raise ValueError("Command contains invalid shell metacharacters")
    
    try:
        # Run the command with security measures:
        # - shell=False to prevent shell injection
        # - capture_output=True to capture stdout/stderr
        # - text=True to get string output instead of bytes
        result = subprocess.run(
            args,
            shell=False,
            capture_output=True,
            text=True,
            check=False  # Don't raise an exception for non-zero exit codes
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Command execution failed: {str(e)}")