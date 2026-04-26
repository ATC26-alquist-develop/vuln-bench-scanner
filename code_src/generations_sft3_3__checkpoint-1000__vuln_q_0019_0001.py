import subprocess
import time
import os

def run_command(command, timeout=300):
    """
    Runs a system command with timeout protection.
    
    Args:
        command (list): Command to execute as a list of arguments
        timeout (int): Maximum execution time in seconds
    
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    if not isinstance(command, list):
        raise ValueError("Command must be provided as a list of arguments")
    
    if not command:
        raise ValueError("Command list cannot be empty")
    
    if not isinstance(timeout, int) or timeout <= 0:
        raise ValueError("Timeout must be a positive integer")
    
    start_time = time.time()
    try:
        # Run command with timeout
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        # Command timed out
        return -1, "", "Command timed out after {} seconds".format(timeout)
    except Exception as e:
        # Handle other exceptions
        return -1, "", str(e)

# Example usage
if __name__ == "__main__":
    # Example command (replace with actual command)
    command = ["ls", "-l"]
    
    # Run command with timeout
    return_code, stdout, stderr = run_command(command)
    
    # Print results
    print(f"Return code: {return_code}")
    print(f"Output: {stdout}")
    print(f"Error: {stderr}")