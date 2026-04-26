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
    return task * 2

def secure_multiprocessing(func: Callable, 
                         input_list: list,
                         max_workers: int = None) -> list:
    """
    A secure implementation of multiprocessing that handles resources safely.
    
    Args:
        func: The function to be executed in parallel
        input_list: List of inputs to be processed
        max_workers: Maximum number of worker processes (default: number of CPU cores)
    
    Returns:
        List of results from processing
    """
    # Validate inputs
    if not callable(func):
        raise TypeError("func must be a callable")
    if not isinstance(input_list, list):
        raise TypeError("input_list must be a list")
    
    # Set safe default for max_workers
    if max_workers is None:
        max_workers = os.cpu_count()
    if not isinstance(max_workers, int) or max_workers <= 0:
        raise ValueError("max_workers must be a positive integer")
    
    # Validate input list size
    if len(input_list) > 10000:  # Reasonable limit for multiprocessing
        raise ValueError("Input list too large for secure multiprocessing")
    
    # Create a pool with a safe number of workers
    with multiprocessing.Pool(processes=min(max_workers, len(input_list))) as pool:
        # Use starmap to pass multiple arguments safely
        results = pool.starmap(func, input_list)
    return results

# Example usage
if __name__ == "__main__":
    # Example task
    def example_task(x):
        return x * x
    
    # Create a list of numbers to process
    numbers = list(range(1000))
    
    # Process numbers using multiprocessing
    start_time = time.time()
    results = secure_multiprocessing(example_task, numbers)
    end_time = time.time()
    
    print(f"Processed {len(numbers)} numbers in {end_time - start_time:.4f} seconds")
    print(f"First 5 results: {results[:5]}")