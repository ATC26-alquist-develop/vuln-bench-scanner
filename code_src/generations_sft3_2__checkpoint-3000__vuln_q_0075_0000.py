import subprocess
import shlex

def run_command(command):
    """
    Safely execute a system command using subprocess.
    
    Args:
        command (str): The command to execute
        
    Returns:
        tuple: (return_code, stdout, stderr)
        
    Raises:
        subprocess.SubprocessError: If command execution fails
    """
    try:
        # Use shlex.split to properly handle command arguments
        cmd_args = shlex.split(command)
        
        # Use subprocess.run with security features enabled
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            check=False,  # Don't raise exception on non-zero exit
            shell=False   # Avoid shell injection vulnerabilities
        )
        
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(f"Command execution failed: {str(e)}")