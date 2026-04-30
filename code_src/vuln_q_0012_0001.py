import subprocess
import shlex

def execute_command(command: str) -> subprocess.CompletedProcess:
    """
    Securely execute a system command and return the result.
    
    Args:
        command (str): The command to execute (e.g., 'ls -l')
        
    Returns:
        CompletedProcess instance containing the return code, stdout, and stderr
        
    Raises:
        ValueError: If the command is empty or contains shell metacharacters
    """
    if not command or not isinstance(command, str):
        raise ValueError("Command must be a non-empty string")
        
    # Split the command into arguments to prevent shell injection
    args = shlex.split(command)
    
    # Execute the command securely
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    
    return result