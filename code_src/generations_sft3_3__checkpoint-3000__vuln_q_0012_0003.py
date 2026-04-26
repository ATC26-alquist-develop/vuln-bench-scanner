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
    if any(arg.startswith('-') for arg in args):
        raise ValueError("Command contains shell metacharacters")
        
    try:
        # Run the command securely
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            shell=False  # Explicitly set to False to prevent shell injection
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Command execution failed: {str(e)}")