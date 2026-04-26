import subprocess
from typing import Optional, Tuple
import shlex

def execute_command(command: str) -> Optional[Tuple[str, str, str]]:
    """
    Securely execute a system command using subprocess.
    
    Args:
        command: Command to execute as a string
        
    Returns:
        Tuple containing (stdout, stderr, return_code) or None if error
    """
    try:
        # Split command into arguments safely
        args = shlex.split(command)
        
        # Validate command is not empty
        if not args:
            return None
            
        # Execute command securely using subprocess
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=30,   # Prevent hanging
            check=False   # Don't raise exception on non-zero exit
        )
        
        return (result.stdout, result.stderr, result.returncode)
        
    except (subprocess.SubprocessError, OSError) as e:
        # Log error here if needed
        return None

# Example usage:
if __name__ == "__main__":
    # Safe command
    stdout, stderr, code = execute_command("ls -l")
    if stdout:
        print("Output:", stdout)
    if stderr:
        print("Error:", stderr)
    print("Return code:", code)