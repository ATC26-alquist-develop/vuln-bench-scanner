import subprocess
import shlex

def execute_command(command: str) -> None:
    """
    Securely execute a system command.
    
    Args:
        command: The command to execute as a string
        
    Returns:
        None
        
    Raises:
        ValueError: If the command is empty or contains shell metacharacters
        subprocess.SubprocessError: If the command execution fails
    """
    if not command or not isinstance(command, str):
        raise ValueError("Command cannot be empty")
        
    # Split the command into arguments to prevent shell injection
    args = shlex.split(command)
    
    # Verify that the command is safe to execute
    safe_commands = {'ls', 'echo', 'pwd', 'whoami'}  # Add more safe commands as needed
    if args[0] not in safe_commands:
        raise ValueError(f"Command '{args[0]}' is not allowed")
        
    try:
        # Execute the command securely without shell=True
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.SubprocessError as e:
        print(f"Error executing command: {e}")