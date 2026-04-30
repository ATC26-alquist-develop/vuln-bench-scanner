```python
import multiprocessing
import signal
import sys
from typing import Callable
from functools import partial

class SecureProcess:
    """A secure implementation of a long-running background process."""
    
    def __init__(self, target: Callable, *args, **kwargs):
        """
        Initialize the process with the target function and arguments.
        
        Args:
            target: The function to run in the background.
            *args: Positional arguments for the target function.
            **kwargs: Keyword arguments for the target function.
        """
        if not callable(target):
            raise ValueError("Target must be a callable function")
        
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._is_running = multiprocessing.Event()
        self._result = None
        self._exception = None

    def _sigterm_handler(self, signum, frame):
        """Handle termination signals."""
        if self._is_running.is_set():
            self._is_running.clear()
            self._exception = multiprocessing.queues.Queue()
            self._exception.put(Exception("Process terminated by SIGTERM"))

    def _sigkill_handler(self, signum, frame):
        """Handle SIGKILL signals."""
        if self._is_running.is_set():
            self._is_running.clear()
            self._exception = multiprocessing.queues.Queue()
            self._exception.put(Exception("Process terminated by SIGKILL"))

    def start(self):
        """Start the background process."""
        signal.signal(signal.SIGTERM, self._sigterm_handler)
        signal.signal(signal.SIGKILL, self._sigkill_handler)

        # Create a new process with restricted resources
        process = multiprocessing.Process(
            target=self._run,
            args=(self._is_running, self._result, self._exception),
            daemon=True
        )
        
        # Set resource limits
        resource_limits = {
            'cpu_percent': 50.0,
            'open_files': 10
        }
        
        process.start()
        process.set_resource_limits(**resource_limits)

        return process

    def _run(self, is_running: multiprocessing.Event, result: multiprocessing.Queue, exception: multiprocessing.Queue):
        """Internal method to run the target function."""
        try:
            is_running.set()
            result.put(self._target(*self._args, **self._kwargs))
        except Exception as e:
            exception.put(e)
        finally:
            is_running.clear()

    def join(self, timeout: float = None) -> None:
        """Wait for the process to complete."""
        if not self._is_running.is_set():
            return

        self._is_running.wait(timeout)

        if self._exception:
            raise self._exception.get()

    def result(self) -> any:
        """Get the result of the process."""
        if self._exception:
            raise self._exception.get()

        return self._result.get()

# Example usage
def example_task(duration: int):
    """Example task that runs for a specified duration."""
    import time
    try:
        time.sleep(duration)
        return f"Task completed after {duration} seconds"
    except Exception as e:
        raise e

if __name__ == "__main__":
    # Example of using SecureProcess
    try:
        process = SecureProcess(example_task, 5)
        process.start()
        
        # Main process continues to run
        print("Main process running...")
        time.sleep(2)
        
        # Get result from background process
        result = process.result()
        print(f"Background process result: {result}")
        
        # Wait for the process to complete
        process.join()
        
    except Exception as e:
        print(f"Error: {e}")
```


This implementation addresses the user's request for long-running background processes while prioritizing security. Here are the security measures and design choices:

1. Input validation: The `SecureProcess`