import subprocess
import shlex

def run_command(command):
    """
    Safely run a shell command and return its output.
    
    Args:
        command (str): The command to run
        
    Returns:
        tuple: (return_code, stdout, stderr)
        
    Raises:
        subprocess.SubprocessError: If the command execution fails
    """
    try:
        # Use shlex.split to properly handle command arguments
        args = shlex.split(command)
        
        # Run command with security measures:
        # - shell=False to prevent shell injection
        # - capture_output=True to capture stdout/stderr
        # - text=True to return strings instead of bytes
        result = subprocess.run(
            args,
            shell=False,
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(f"Command execution failed: {str(e)}")