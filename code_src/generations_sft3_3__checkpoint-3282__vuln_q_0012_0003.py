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
        
        # Run the command with security measures:
        # - shell=False to prevent shell injection
        # - capture_output=True to capture stdout/stderr
        # - text=True to get string output instead of bytes
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

# ===== cell separator =====

try:
    return_code, stdout, stderr = run_command("ls -l")
    print(f"Return Code: {return_code}")
    print(f"Output: {stdout}")
    print(f"Errors: {stderr}")
except subprocess.SubprocessError as e:
    print(f"Error: {str(e)}")