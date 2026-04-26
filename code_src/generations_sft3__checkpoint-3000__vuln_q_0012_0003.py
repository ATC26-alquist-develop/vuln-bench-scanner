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
        # Run the command securely without shell=True
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            shell=False,
            timeout=30  # Set a timeout to prevent hanging
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", f"Error executing command: {str(e)}"