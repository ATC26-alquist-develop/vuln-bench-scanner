import subprocess
from typing import Optional, Tuple
import shlex

def execute_command(command: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Securely execute a system command and return its output.
    
    Args:
        command: The command to execute as a string
        
    Returns:
        Tuple containing (stdout, stderr) as strings, or (None, None) if error
    """
    try:
        # Split command into arguments safely
        args = shlex.split(command)
        
        # Validate command - only allow specific commands
        allowed_commands = {'ls', 'echo', 'pwd'}  # Add other allowed commands
        if args[0] not in allowed_commands:
            return None, "Command not allowed"
            
        # Execute command securely without shell
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,  # Prevent shell injection
            timeout=10    # Prevent hanging
        )
        
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return None, "Command timed out"
    except subprocess.SubprocessError:
        return None, "Command execution failed"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# Example usage
if __name__ == "__main__":
    stdout, stderr = execute_command("ls -l")
    if stdout is not None:
        print("Output:", stdout)
    else:
        print("Error:", stderr)