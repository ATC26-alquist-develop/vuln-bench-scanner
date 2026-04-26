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
        print(f"Command timed out after {timeout} seconds")
        return 1, "", "Command timed out"
    except Exception as e:
        print(f"Error executing command: {str(e)}")
        return 1, "", str(e)

def main():
    # Example usage
    command = ['ls', '-l']
    return_code, stdout, stderr = run_command(command)
    
    if return_code == 0:
        print("Command output:")
        print(stdout)
    else:
        print(f"Command failed with error: {stderr}")

if __name__ == "__main__":
    main()