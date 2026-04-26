import subprocess
import time
import os

def run_command(command, timeout=300):
    """
    Runs a system command with timeout protection.
    
    Args:
        command (str): The command to execute
        timeout (int): Maximum execution time in seconds
    
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    if not isinstance(command, str) or not command.strip():
        raise ValueError("Command must be a non-empty string")
    
    if not isinstance(timeout, int) or timeout <= 0:
        raise ValueError("Timeout must be a positive integer")
    
    try:
        # Use subprocess.run with shell=False for security
        result = subprocess.run(
            command,
            shell=False,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out after {} seconds".format(timeout)
    except Exception as e:
        return -1, "", "Error executing command: {}".format(str(e))

# Example usage
if __name__ == "__main__":
    command = "ls -l /tmp"
    return_code, stdout, stderr = run_command(command)
    print(f"Return code: {return_code}")
    print(f"Output: {stdout}")
    print(f"Error: {stderr}")