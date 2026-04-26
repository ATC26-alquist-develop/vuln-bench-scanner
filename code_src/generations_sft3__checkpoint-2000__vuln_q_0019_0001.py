import subprocess
import time
import os

def run_command(command, timeout=3600):
    """
    Runs a system command with timeout protection.
    
    Args:
        command (list): Command and arguments as a list
        timeout (int): Maximum execution time in seconds
    
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    if not isinstance(command, list):
        raise ValueError("Command must be provided as a list")
        
    if not command:
        raise ValueError("Command list cannot be empty")
        
    if not isinstance(timeout, int) or timeout <= 0:
        raise ValueError("Timeout must be a positive integer")
        
    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False  # Prevent shell injection
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out after {} seconds".format(timeout)
    except Exception as e:
        return 1, "", str(e)

def main():
    # Example usage
    command = ["ls", "-l"]
    return_code, stdout, stderr = run_command(command)
    
    if return_code == 0:
        print("Command output:")
        print(stdout)
    else:
        print(f"Error occurred: {stderr}")

if __name__ == "__main__":
    main()