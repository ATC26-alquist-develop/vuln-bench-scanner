import subprocess
import time
import os

def run_command_with_timeout(command: list[str], timeout: int) -> tuple[str, str, int]:
    """
    Runs a command in a separate process with a timeout.
    
    Args:
        command: List of command arguments
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr, return_code)
        
    Raises:
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: If command execution fails
    """
    try:
        # Run command in a separate process group
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,  # Prevent shell injection
            preexec_fn=os.setsid  # Set process group
        )
        
        # Start timer
        start_time = time.time()
        
        # Wait for command to complete or timeout
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # Terminate process group
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            raise
            
        # Get execution time
        exec_time = int(time.time() - start_time)
        
        return stdout.decode('utf-8'), stderr.decode('utf-8'), process.returncode, exec_time
        
    except subprocess.SubprocessError as e:
        raise