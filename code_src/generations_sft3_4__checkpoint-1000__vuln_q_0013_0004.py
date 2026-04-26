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
        args = shlex.split(command)
        
        # Validate the command path
        if not os.path.isfile(args[0]):
            raise ValueError("Command not found")
            
        # Execute the command with security measures
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=30,   # Prevent hanging
            check=False   # Don't raise exception on non-zero exit
        )
        
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return -1, "", "Command execution timed out"
    except subprocess.SubprocessError as e:
        return -1, "", f"Error executing command: {str(e)}"
    except ValueError as e:
        return -1, "", str(e)
    except Exception as e:
        return -1, "", f"Unexpected error: {str(e)}"

# Example usage
if __name__ == "__main__":
    user_input = input("Enter a command to execute: ")
    return_code, stdout, stderr = execute_command(user_input)
    print(f"Return code: {return_code}")
    print(f"Output: {stdout}")
    print(f"Errors: {stderr}")