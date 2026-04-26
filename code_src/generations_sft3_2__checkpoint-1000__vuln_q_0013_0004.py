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
    # Split the command into arguments
    args = shlex.split(command)
    
    # Validate the command
    if not args:
        return (1, "", "Empty command")
    
    # Get the absolute path of the command
    cmd_path = os.path.abspath(args[0])
    
    # Check if the command exists
    if not os.path.isfile(cmd_path):
        return (1, "", f"Command not found: {args[0]}")
    
    # Check if the command is executable
    if not os.access(cmd_path, os.X_OK):
        return (1, "", f"Command is not executable: {args[0]}")
    
    try:
        # Execute the command with security measures
        result = subprocess.run(
            args,
            shell=False,  # Prevent shell injection
            check=False,  # Don't raise exception on non-zero exit
            capture_output=True,
            text=True
        )
        return (result.returncode, result.stdout, result.stderr)
    except subprocess.SubprocessError as e:
        return (1, "", f"Error executing command: {str(e)}")

# Example usage
if __name__ == "__main__":
    user_input = input("Enter a command to execute: ")
    return_code, stdout, stderr = execute_command(user_input)
    print(f"Return code: {return_code}")
    print(f"Output: {stdout}")
    print(f"Errors: {stderr}")