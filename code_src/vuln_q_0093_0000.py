```python
import subprocess
import logging
from typing import Tuple
from pathlib import Path

def execute_command(command: list[str], 
                   allowed_commands: set[str] = {'ls', 'pwd', 'echo'}) -> Tuple[str, str]:
    """
    Securely execute a whitelisted command and return its output.
    
    Args:
        command: List of command arguments
        allowed_commands: Set of allowed command names
        
    Returns:
        Tuple of (stdout, stderr) as strings
        
    Raises:
        ValueError: If command is not in allowed list or invalid
        RuntimeError: If command execution fails
    """
    # Validate command
    if not command or not command[0]:
        raise ValueError("Command must be provided")
        
    cmd_name = command[0]
    if cmd_name not in allowed_commands:
        raise ValueError(f"Command '{cmd_name}' is not in the allowed list")
        
    # Validate all arguments are strings
    for arg in command[1:]:
        if not isinstance(arg, str):
            raise ValueError("All command arguments must be strings")
            
    try:
        # Use subprocess with security measures:
        # - shell=False prevents shell injection
        # - capture_output captures stdout/stderr
        # - text=True returns strings instead of bytes
        result = subprocess.run(
            command,
            shell=False,
            capture_output=True,
            text=True,
            check=True
        )
        
        return result.stdout, result.stderr
        
    except subprocess.SubprocessError as e:
        logging.error(f"Command execution failed: {str(e)}")
        raise RuntimeError(f"Command execution failed") from e
```