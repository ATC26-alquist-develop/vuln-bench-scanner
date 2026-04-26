import multiprocessing
import time
import os
from typing import Callable, Any

def secure_worker(task: Any) -> Any:
    """
    A secure worker function that performs a single task.
    This function should contain your actual CPU-intensive task.
    """
    # Simulating work
    time.sleep(0.1)
    return task

def secure_multiprocessing(
    tasks: list,
    num_processes: int = None,
    timeout: int = 30
) -> list:
    """
    Secure implementation of multiprocessing for CPU-intensive tasks.
    
    Args:
        tasks: List of tasks to process
        num_processes: Number of processes to use (default: number of CPU cores)
        timeout: Maximum execution time for each process
    
    Returns:
        List of results from processed tasks
    """
    # Validate inputs
    if not isinstance(tasks, list):
        raise ValueError("Tasks must be provided as a list")
    if num_processes is not None and not isinstance(num_processes, int):
        raise ValueError("Number of processes must be an integer or None")
    if num_processes is not None and num_processes <= 0:
        raise ValueError("Number of processes must be positive")
    if timeout <= 0:
        raise ValueError("Timeout must be positive")

    # Set number of processes if not provided
    num_processes = num_processes or multiprocessing.cpu_count()

    # Validate timeout
    if timeout > 3600:  # Prevent extremely long timeouts
        raise ValueError("Timeout value too high")

    # Create secure process pool
    with multiprocessing.Pool(processes=num_processes, initializer=_worker_initializer) as pool:
        try:
            # Process tasks with timeout
            results = pool.map(secure_worker, tasks, timeout=timeout)
            return results
        except multiprocessing.TimeoutError:
            raise TimeoutError("Process pool operation timed out")
        except Exception as e:
            raise RuntimeError(f"Process pool operation failed: {str(e)}")

def _worker_initializer():
    """
    Secure process initializer that resets global state.
    """
    # Reset any global state that could be affected by multiprocessing
    # This is a basic example - adjust based on your specific needs
    global _global_state
    _global_state = None

# Example usage
if __name__ == "__main__":
    # Example CPU-intensive task
    def example_task(x):
        return x * 2

    # Create a list of tasks
    tasks = [i for i in range(100)]

    try:
        # Run multiprocessing
        results = secure_multiprocessing(tasks, num_processes=4)
        
        # Process results
        for i, result in enumerate(results):
            print(f"Result {i}: {result}")
            
    except (ValueError, TimeoutError, RuntimeError) as e:
        print(f"Error: {str(e)}")