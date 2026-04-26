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
        subprocess.SubprocessError: If the command execution fails
    """
    try:
        # Split the command into arguments safely
        args = shlex.split(command)
        
        # Run the command with security measures
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(f"Command execution failed: {str(e)}")