```python
import subprocess
import logging
from typing import Tuple
from pathlib import Path

def run_command(command: list[str], 
                working_dir: Path = None,
                timeout: int = 5) -> Tuple[str, str]:
    """
    Securely run an external command and capture its output.
    
    Args:
        command: List of command arguments (not shell string)
        working_dir: Optional working directory (must exist)
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout, stderr) as strings
        
    Raises:
        ValueError: If command is invalid
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.SubprocessError: For other subprocess-related errors
    """
    # Input validation
    if not command or not isinstance(command, list):
        raise ValueError("Command must be a non-empty list")
        
    if working_dir:
        working_dir = Path(working_dir)
        if not working_dir.exists():
            raise ValueError("Working directory must exist")
            
    try:
        # Run command securely without shell
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,  # Prevent shell injection
            cwd=working_dir,
            text=True,
            # Restrict resource usage
            preexec_fn=lambda: (
                import resource
                resource.setrlimit(resource.RLIMIT_CPU, (timeout, timeout))
                resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
            )
        ) as process:
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                
                if process.returncode != 0:
                    raise subprocess.SubprocessError(
                        f"Command failed with return code {process.returncode}"
                    )
                
                return stdout, stderr
                
            except subprocess.TimeoutExpired:
                process.kill()
                raise subprocess.TimeoutExpired(
                    process,
                    timeout,
                    output=stdout,
                    stderr=stderr
                )
                
    except (OSError, ValueError) as e:
        logging.error(f"Error running command: {str(e)}")
        raise
```