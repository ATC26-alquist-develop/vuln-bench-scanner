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
        
        # Check if command completed within timeout
        if time.time() - start_time > timeout:
            raise TimeoutError("Command execution exceeded timeout")
            
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        raise TimeoutError("Command execution exceeded timeout")
    except Exception as e:
        raise RuntimeError(f"Command execution failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        # Example command (replace with actual command)
        command = ["ls", "-l"]
        
        # Run command with timeout
        return_code, stdout, stderr = run_command(command)
        
        print(f"Return code: {return_code}")
        print(f"Output: {stdout}")
        print(f"Errors: {stderr}")
        
    except TimeoutError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")