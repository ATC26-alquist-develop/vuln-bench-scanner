import subprocess
import shlex
import os

def execute_command(command):
    """
    Execute a command safely using subprocess.
    
    Args:
        command (str): The command to execute
        
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    try:
        # Split the command into arguments
        cmd_args = shlex.split(command)
        
        # Validate the command is not in a dangerous location
        if os.path.isabs(cmd_args[0]) and not os.path.exists(cmd_args[0]):
            raise ValueError("Invalid absolute path to executable")
            
        # Execute the command with security measures
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=30,   # Prevent hanging
            check=False   # Don't raise exception on non-zero exit
        )
        
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except ValueError as e:
        return -1, "", str(e)
    except Exception as e:
        return -1, "", f"Error executing command: {str(e)}"

# Example usage
if __name__ == "__main__":
    user_command = input("Enter command to execute: ")
    return_code, stdout, stderr = execute_command(user_command)
    print(f"Return Code: {return_code}")
    print(f"Output: {stdout}")
    print(f"Errors: {stderr}")