import subprocess
import time
import os

def run_command(command, timeout=60):
    """
    Runs a command with timeout protection.
    
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
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        while process.poll() is None:
            if time.time() - start_time > timeout:
                process.terminate()
                process.wait(timeout=5)
                return (1, "", "Process timed out")
            time.sleep(0.1)
    except subprocess.TimeoutExpired:
        process.terminate()
        process.wait(timeout=5)
        return (1, "", "Process timed out")
        
    return_code = process.returncode
    stdout, stderr = process.communicate()
    
    return (return_code, stdout.decode('utf-8', errors='replace'), stderr.decode('utf-8', errors='replace'))

# Example usage
if __name__ == "__main__":
    try:
        result = run_command(["ls", "-l"])
        print(f"Return code: {result[0]}")
        print(f"Output: {result[1]}")
        print(f"Errors: {result[2]}")
    except Exception as e:
        print(f"Error: {str(e)}")