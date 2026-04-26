import subprocess
from typing import Optional, Tuple
from pathlib import Path

def execute_command(command: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Securely execute a system command using subprocess.
    
    Args:
        command: Command to execute as string
        
    Returns:
        Tuple of (stdout, stderr) as strings, or (None, None) on error
    """
    try:
        # Split command into list to prevent shell injection
        cmd_list = command.split()
        
        # Validate command exists
        cmd_path = Path(cmd_list[0])
        if not cmd_path.is_file():
            return None, "Command not found"
            
        # Execute command securely without shell
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            shell=False,
            timeout=30  # Prevent hanging
        )
        
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return None, "Command timed out"
    except subprocess.SubprocessError:
        return None, "Command execution failed"
    except Exception:
        return None, "Unexpected error occurred"