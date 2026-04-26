import multiprocessing
import time
import os
from typing import Callable, Any

def secure_worker(task: Any) -> Any:
    """
    A secure worker function that performs a simple CPU-bound task.
    This function is designed to be safe and doesn't introduce vulnerabilities.
    
    Args:
        task: Any object that can be safely processed
        
    Returns:
        The result of processing the task
    """
    # Simulate CPU intensive work
    time.sleep(0.1)
    return task

def secure_multiprocessing(func: Callable, 
                         data: list,
                         num_processes: int = None) -> list:
    """
    A secure implementation of multiprocessing for CPU-bound tasks.
    
    Args:
        func: The function to be executed in parallel
        data: List of data to be processed
        num_processes: Number of processes to use (default: number of CPU cores)
        
    Returns:
        List of results from the parallel processing
        
    Raises:
        ValueError: If num_processes is set too high
        TypeError: If inputs are of incorrect type
    """
    # Input validation
    if not callable(func):
        raise TypeError("func must be a callable")
    if not isinstance(data, list):
        raise TypeError("data must be a list")
    if num_processes is not None:
        if not isinstance(num_processes, int):
            raise TypeError("num_processes must be an integer")
        if num_processes < 1:
            raise ValueError("num_processes must be positive")
        if num_processes > os.cpu_count():
            raise ValueError("num_processes cannot exceed number of CPU cores")

    # Create a pool of workers
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Use starmap to pass multiple arguments to the function
        results = pool.starmap(func, [(item,) for item in data])
    return results

# Example usage
def main():
    # Example data
    data = list(range(100))
    
    # Process data using 4 processes (half the CPU cores)
    results = secure_multiprocessing(secure_worker, data, num_processes=4)
    
    # Verify results
    assert len(results) == 100
    assert all(isinstance(r, int) for r in results)
    assert all(r == i for i, r in enumerate(results))

if __name__ == "__main__":
    main()