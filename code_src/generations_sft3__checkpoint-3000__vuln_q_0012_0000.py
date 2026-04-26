import subprocess
from typing import Tuple
import os

def run_command(command: list[str], timeout: int = 30) -> Tuple[str, str, int]:
    """
    Securely run an external command and capture its output.
    
    Args:
        command: List of command arguments (first item is the program)
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr, return_code)
        
    Raises:
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: If command fails to execute
    """
    try:
        # Run command with security measures:
        # - shell=False to prevent shell injection
        # - timeout to prevent hanging
        # - capture_output=True to capture stdout/stderr
        # - text=True for string output
        result = subprocess.run(
            command,
            shell=False,
            timeout=timeout,
            capture_output=True,
            text=True
        )
        
        return result.stdout, result.stderr, result.returncode

    except subprocess.TimeoutExpired as e:
        raise subprocess.TimeoutExpired(
            cmd=command,
            timeout=timeout,
            output=e.output,
            stderr=e.stderr
        )
    except subprocess.SubprocessError as e:
        raise

def is_safe_command(command: list[str]) -> bool:
    """
    Validate if the command is safe to execute.
    
    Args:
        command: List of command arguments
        
    Returns:
        bool: True if command is safe, False otherwise
    """
    # Whitelist of allowed commands
    ALLOWED_COMMANDS = {
        'ls', 'echo', 'pwd', 'date', 'whoami'
    }
    
    # Check if command is in whitelist
    if not command or not isinstance(command, list):
        return False
        
    base_command = command[0]
    return base_command in ALLOWED_COMMANDS

def run_safe_command(command: str) -> Tuple[str, str, int]:
    """
    Run a safe command with security measures.
    
    Args:
        command: Command string to execute
        
    Returns:
        Tuple of (stdout, stderr, return_code)
        
    Raises:
        ValueError: If command is not safe
        subprocess.SubprocessError: If command fails to execute
    """
    if not isinstance(command, str):
        raise ValueError("Command must be a string")
        
    # Split command into list of arguments
    command_list = command.split()
    
    # Validate command
    if not is_safe_command(command_list):
        raise ValueError("Command not in whitelist of safe commands")
    
    # Run command with security measures
    return run_command(command_list)