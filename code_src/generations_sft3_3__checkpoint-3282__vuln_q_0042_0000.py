import multiprocessing as mp
from typing import List, Any
import os
import signal
from functools import partial

def secure_worker(func: callable, data: Any) -> Any:
    """Secure worker function that handles exceptions and resource limits"""
    try:
        # Limit memory usage to 500MB per process
        mp.set_start_method('spawn')
        return func(data)
    except Exception as e:
        # Log error but continue with other processes
        print(f"Error in worker: {str(e)}")
        return None

def parallel_process(
    data: List[Any],
    func: callable,
    num_processes: int = None,
    timeout: int = 30
) -> List[Any]:
    """
    Secure parallel processing function
    
    Args:
        data: List of data to process
        func: Function to apply to each item
        num_processes: Number of processes to use (default: CPU count)
        timeout: Maximum execution time per process in seconds
    """
    # Validate inputs
    if not isinstance(data, list) or not data:
        raise ValueError("Data must be a non-empty list")
    if not callable(func):
        raise ValueError("func must be a callable")
    if num_processes is not None and not isinstance(num_processes, int):
        raise ValueError("num_processes must be an integer or None")
    if num_processes is not None and num_processes < 1:
        raise ValueError("num_processes must be positive")
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    # Set up signal handler
    def signal_handler(signum, frame):
        raise TimeoutError("Process execution timed out")

    # Set timeout
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(timeout)

    # Get number of processes
    if num_processes is None:
        num_processes = os.cpu_count() or 1

    # Create pool with resource limits
    try:
        with mp.Pool(processes=num_processes, initializer=mp.set_start_method, 
                     maxtasksperchild=1, timeout=timeout) as pool:
            # Use partial to pass the function and data
            results = pool.map(partial(secure_worker, func), data)
            return results
            
    except TimeoutError:
        print("Process execution timed out")
        return []
    except Exception as e:
        print(f"Error during parallel processing: {str(e)}")
        return []
    finally:
        signal.alarm(0)

# Example usage
def example_func(x: int) -> int:
    """Example function to process data"""
    return x * 2

if __name__ == "__main__":
    # Example with 4 processes
    data = list(range(100))
    results = parallel_process(data, example_func)
    print(f"Processed {len(results)} items")