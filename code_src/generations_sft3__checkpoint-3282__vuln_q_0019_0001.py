import subprocess
import time
import os

def run_command(command, timeout=60):
    """
    Runs a command with timeout protection.
    
    Args:
        command: Command to run as a list of strings
        timeout: Maximum execution time in seconds
    
    Returns:
        Tuple of (return_code, stdout, stderr)
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
        print(f"Error running command: {str(e)}")
        return 1, "", str(e)

# Example usage
if __name__ == "__main__":
    # Example command
    command = ["ls", "-l"]
    
    # Run command with timeout
    return_code, stdout, stderr = run_command(command)
    
    # Print results
    print(f"Return code: {return_code}")
    print(f"Output: {stdout}")
    print(f"Error: {stderr}")