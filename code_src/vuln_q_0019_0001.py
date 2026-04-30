import subprocess
import time
from typing import Optional

def run_command_with_timeout(
    command: list[str],
    timeout_seconds: int = 30,
    interval_seconds: int = 1
) -> Optional[str]:
    """
    Run a command with a timeout.
    
    Args:
        command: List of command arguments
        timeout_seconds: Maximum execution time in seconds
        interval_seconds: Time to wait between checks in seconds
        
    Returns:
        Command output if successful, None if timeout or error
    """
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,  # Security: don't use shell
            text=True
        )
        
        start_time = time.time()
        while process.poll() is None:
            if time.time() - start_time > timeout_seconds:
                process.kill()
                return None
            time.sleep(interval_seconds)
            
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            return None
        return stdout
        
    except Exception:
        return None