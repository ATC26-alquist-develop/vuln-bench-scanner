import multiprocessing
import time
import os
from typing import Callable, Any

def secure_worker(task: Any) -> Any:
    """
    A secure worker function that performs a simple CPU-bound task.
    This function is designed to be safe and doesn't introduce vulnerabilities.
    """
    # Simulate CPU-intensive task
    result = 0
    for i in range(1000000):
        result += i
    return result

def secure_multiprocessing(func: Callable, num_processes: int) -> tuple:
    """
    A secure implementation of multiprocessing for CPU-bound tasks.
    
    Args:
        func: The function to be executed in parallel
        num_processes: Number of processes to spawn (1-4 recommended)
    
    Returns:
        Tuple of (total result, execution time)
    """
    # Validate input parameters
    if not callable(func):
        raise TypeError("func must be a callable")
    
    if not isinstance(num_processes, int):
        raise TypeError("num_processes must be an integer")
        
    if num_processes < 1 or num_processes > 4:
        raise ValueError("num_processes must be between 1 and 4")

    # Set up multiprocessing pool with a safe number of processes
    processes = min(num_processes, os.cpu_count() or 1)
    pool = multiprocessing.Pool(processes=processes)
    
    try:
        # Create tasks
        tasks = [pool.apply_async(secure_worker) for _ in range(processes)]
        
        # Get results
        results = [task.get() for task in tasks]
        
        # Calculate total result
        total_result = sum(results)
        
        # Measure execution time
        start_time = time.time()
        pool.close()
        pool.join()
        
        return total_result, time.time() - start_time
    
    except Exception as e:
        # Ensure proper cleanup
        pool.close()
        pool.join()
        raise e

# Example usage
if __name__ == "__main__":
    try:
        result, duration = secure_multiprocessing(secure_worker, 4)
        print(f"Result: {result}")
        print(f"Execution time: {duration:.4f} seconds")
    except Exception as e:
        print(f"Error: {e}")