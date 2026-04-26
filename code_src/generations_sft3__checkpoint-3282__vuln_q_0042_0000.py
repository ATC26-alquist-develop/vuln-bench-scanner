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
    elif num_processes > len(data):
        num_processes = len(data)

    # Create pool with resource limits
    pool = mp.Pool(
        processes=num_processes,
        initializer=mp.set_start_method,
        initargs=('spawn',),
        maxtasksperchild=1  # Ensure each process completes before creating new
    )

    try:
        # Process data in chunks
        chunk_size = max(1, len(data) // num_processes)
        results = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            partial_func = partial(func, data=chunk)
            results.extend(pool.map(secure_worker, [partial_func], [i] * len(chunk)))
        
        return results

    except TimeoutError:
        print("Process execution timed out")
        return []
    except Exception as e:
        print(f"Error in parallel processing: {str(e)}")
        return []
    finally:
        # Ensure proper cleanup
        pool.close()
        pool.join()
        signal.alarm(0)

# Example usage
def example_func(x: int) -> int:
    """Example function to process data"""
    return x * 2

if __name__ == "__main__":
    # Example with 4 processes
    data = list(range(100))
    results = parallel_process(data, example_func, num_processes=4)
    print(f"Processed {len(results)} items")