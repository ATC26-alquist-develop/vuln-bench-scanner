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
                         input_list: list, 
                         max_workers: int = None) -> list:
    """
    A secure implementation of multiprocessing for CPU-bound tasks.
    
    Args:
        func: The function to be executed in parallel
        input_list: List of inputs to be processed
        max_workers: Maximum number of worker processes to use
        
    Returns:
        List of results from the processed inputs
        
    Raises:
        ValueError: If inputs are invalid
        RuntimeError: If multiprocessing fails
    """
    # Input validation
    if not callable(func):
        raise ValueError("func must be a callable")
    if not isinstance(input_list, list):
        raise ValueError("input_list must be a list")
    if max_workers is not None and not isinstance(max_workers, int):
        raise ValueError("max_workers must be None or an integer")
        
    # Set reasonable default for max_workers
    max_workers = max_workers or multiprocessing.cpu_count()
    
    # Create a pool with a reasonable size
    with multiprocessing.Pool(processes=min(max_workers, os.cpu_count() or 1)) as pool:
        # Use starmap to pass multiple arguments
        results = pool.starmap(func, [(item,) for item in input_list])
    return results

# Example usage
def main():
    # Example CPU intensive task
    def example_task(x):
        return x * 2

    # Create a list of numbers to process
    numbers = list(range(1000))

    # Process numbers using multiprocessing
    start_time = time.time()
    results = secure_multiprocessing(example_task, numbers)
    end_time = time.time()

    print(f"Processed {len(results)} items in {end_time - start_time:.2f} seconds")
    print(f"First 5 results: {results[:5]}")

if __name__ == "__main__":
    main()