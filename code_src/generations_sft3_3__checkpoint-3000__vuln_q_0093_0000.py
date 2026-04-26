import subprocess
import shlex

def execute_command(command):
    """
    Safely execute a system command and return its output.
    
    Args:
        command (str): The command to execute
        
    Returns:
        tuple: (return_code, stdout, stderr)
        
    Raises:
        subprocess.SubprocessError: If command execution fails
    """
    try:
        # Split command into arguments safely
        args = shlex.split(command)
        
        # Execute command safely without shell=True
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,
            timeout=30  # Set timeout to prevent hanging
        )
        
        return (result.returncode, result.stdout, result.stderr)
        
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(f"Command execution failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")