import subprocess
import signal
import time
from typing import Optional, Tuple

def run_command_with_timeout(
    command: list[str],
    timeout_seconds: int = 30,
    working_dir: Optional[str] = None,
    shell: bool = False
) -> Tuple[Optional[subprocess.CompletedProcess], Optional[float]]:
    """
    Run a command with a timeout.
    
    Args:
        command: List of command arguments
        timeout_seconds: Maximum execution time in seconds
        working_dir: Working directory for command execution
        shell: Whether to use shell
    
    Returns:
        Tuple of (completed process, execution time) or (None, None) if timeout
    """
    try:
        # Start process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
            cwd=working_dir,
            start_new_session=True
        )
        
        # Wait for process to complete or timeout
        try:
            # Set timeout
            timeout = time.time() + timeout_seconds
            
            # Wait for process to complete
            stdout, stderr = process.communicate(timeout=timeout - time.time())
            
            # Calculate execution time
            execution_time = time.time() - timeout
            
            return process, execution_time
            
        except subprocess.TimeoutExpired:
            # Kill process if timeout
            process.kill()
            return None, None
            
    except Exception as e:
        # Handle exceptions
        return None, None