import subprocess
import shlex

def run_command(command):
    """
    Securely run a shell command and return its output.
    
    Args:
        command (str): The command to run
        
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    try:
        # Use shlex.split to properly handle command arguments
        cmd_args = shlex.split(command)
        
        # Run command with security measures:
        # shell=False: Prevents shell injection
        # text=True: Return string output instead of bytes
        # capture_output=True: Capture stdout and stderr
        # text=True: Ensure output is string
        result = subprocess.run(
            cmd_args,
            shell=False,
            text=True,
            capture_output=True,
            check=False  # Don't raise exception on non-zero exit
        )
        
        return result.returncode, result.stdout, result.stderr
    except subprocess.SubprocessError as e:
        # Handle subprocess errors
        return -1, "", f"Error running command: {str(e)}"

# Example usage:
# return_code, stdout, stderr = run_command("ls -l")
# print(f"Return code: {return_code}")
# print(f"Output: {stdout}")
# print(f"Errors: {stderr}")