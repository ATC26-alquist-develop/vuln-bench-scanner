import subprocess
import signal
import threading
from typing import List, Optional
from pathlib import Path

def run_with_timeout(command: List[str], timeout_seconds: int = 30) -> Optional[str]:
    """
    Run a command with a timeout and return its output.
    
    Args:
        command: List of command arguments (first item is the program)
        timeout_seconds: Maximum time to wait for command completion
        
    Returns:
        Command output as string if completed, None if timed out
    """
    if not command or not isinstance(command, list):
        raise ValueError("Command must be a non-empty list")
        
    if not isinstance(timeout_seconds, int) or timeout_seconds <= 0:
        raise ValueError("Timeout must be a positive integer")

    # Validate command exists and is executable
    cmd_path = Path(command[0])
    if not cmd_path.exists() or not cmd_path.is_file():
        raise FileNotFoundError(f"Command not found: {command[0]}")
        
    # Create a subprocess with controlled output
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,  # Prevent shell injection
        text=True,
        # Pass SIGTERM signal to child process on termination
        preexec_fn=lambda: signal.signal(signal.SIGTERM, signal.SIG_DFL)
    )

    # Store output for later
    output = []
    output_lock = threading.Lock()

    def collect_output():
        with open('output.txt', 'w') as f:
            while True:
                with output_lock:
                    if process.poll() is not None:
                        break
                    try:
                        line = process.stdout.readline()
                        if line:
                            f.write(line)
                            f.flush()
                        else:
                            break
                    except Exception as e:
                        raise RuntimeError(f"Error reading process output: {e}")

    # Start output collection in a separate thread
    output_thread = threading.Thread(target=collect_output)
    output_thread.start()

    try:
        # Wait for completion or timeout
        process.wait(timeout=timeout_seconds)
        
        # If process completed, return output
        if process.returncode == 0:
            return ''.join(output)
        else:
            return None
    except subprocess.TimeoutExpired:
        # If timeout occurred, terminate the process
        process.terminate()
        try:
            process.wait(timeout=1)  # Wait for process to terminate
        except subprocess.TimeoutExpired:
            process.kill()
        
        return None
    finally:
        # Ensure thread is cleaned up
        if output_thread.is_alive():
            output_thread.join()