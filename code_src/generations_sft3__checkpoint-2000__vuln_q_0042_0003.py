import multiprocessing
import time
import os
from typing import Callable, Any

def secure_worker(task: Any) -> Any:
    """
    A secure worker function that performs a simple CPU-bound task.
    This function is designed to be safe and doesn't introduce any vulnerabilities.
    
    Args:
        task: Any data to process
        
    Returns:
        Processed result
        
    Raises:
        ValueError: If input is invalid
    """
    if not isinstance(task, (int, float, str, bytes)):
        raise ValueError("Invalid input type")
        
    # Simulate CPU-intensive task
    result = 0
    for i in range(1000000):
        result += i * task
    
    return result

def secure_multiprocessing(func: Callable, 
                         data: list,
                         num_processes: int = None) -> list:
    """
    Securely process data using multiprocessing.
    
    Args:
        func: Function to process data
        data: List of data to process
        num_processes: Number of processes to use (default: number of CPU cores)
        
    Returns:
        List of results
        
    Raises:
        ValueError: If inputs are invalid
    """
    # Validate inputs
    if not callable(func):
        raise ValueError("First argument must be a callable function")
        
    if not isinstance(data, list):
        raise ValueError("Data must be provided as a list")
        
    if num_processes is not None:
        if not isinstance(num_processes, int):
            raise ValueError("Number of processes must be an integer")
        if num_processes < 1:
            raise ValueError("Number of processes must be positive")
            
    # Set number of processes safely
    if num_processes is None:
        num_processes = os.cpu_count()
    elif num_processes > os.cpu_count():
        num_processes = os.cpu_count()
        
    # Create a pool of workers
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Process data in parallel
        results = pool.map(func, data)
        
    return results

# Example usage
if __name__ == "__main__":
    # Example data
    data = [1, 2, 3, 4, 5]
    
    # Process data using multiprocessing
    start_time = time.time()
    results = secure_multiprocessing(secure_worker, data)
    end_time = time.time()
    
    print(f"Results: {results}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")