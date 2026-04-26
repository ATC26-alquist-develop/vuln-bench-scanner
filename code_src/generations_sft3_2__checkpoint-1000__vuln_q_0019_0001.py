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
    
    try:
        start_time = time.time()
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        end_time = time.time()
        
        if end_time - start_time > timeout:
            raise TimeoutError("Command execution exceeded timeout")
        
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        raise TimeoutError("Command execution timed out")
    except Exception as e:
        raise RuntimeError(f"Error executing command: {str(e)}")

# Example usage:
if __name__ == "__main__":
    try:
        # Example command: sleep for 10 seconds
        return_code, stdout, stderr = run_command(["sleep", "10"])
        print(f"Return code: {return_code}")
        print(f"Output: {stdout}")
        print(f"Errors: {stderr}")
    except (TimeoutError, RuntimeError) as e:
        print(f"Error: {str(e)}")