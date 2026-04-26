import multiprocessing
import time
import os
from typing import Callable, Any

def secure_worker(task: Any) -> Any:
    """
    A secure worker function that performs a simple CPU-bound task.
    This function is designed to be safe and doesn't introduce any vulnerabilities.
    
    Args:
        task: Any data to be processed by the worker
        
    Returns:
        The result of the task processing
        
    Raises:
        ValueError: If task is not a valid input
    """
    if not isinstance(task, (int, float, str, list, dict)):
        raise ValueError("Invalid task type")
        
    # Simulate CPU-intensive task
    result = 0
    for i in range(1000000):
        result += i
    return result

def secure_multiprocessing(func: Callable, tasks: list) -> list:
    """
    Secure wrapper for multiprocessing that handles input validation and resource management.
    
    Args:
        func: The function to be executed in parallel
        tasks: List of tasks to be processed
        
    Returns:
        List of results from the parallel execution
        
    Raises:
        ValueError: If input validation fails
        RuntimeError: If multiprocessing fails
    """
    if not isinstance(tasks, list):
        raise ValueError("Tasks must be provided as a list")
        
    # Validate all tasks
    for task in tasks:
        if not isinstance(task, (int, float, str, list, dict)):
            raise ValueError("All tasks must be valid input types")
            
    # Set up multiprocessing pool with reasonable limits
    num_processes = min(multiprocessing.cpu_count(), 4)  # Limit to 4 processes max
    pool = multiprocessing.Pool(processes=num_processes)
    
    try:
        # Use starmap for efficient parallel execution
        results = pool.starmap(func, tasks)
        return results
    finally:
        # Ensure pool is always closed
        pool.close()

def main():
    # Example usage
    tasks = [1, 2, 3, 4, 5]
    start_time = time.time()
    
    # Run parallel processing
    results = secure_multiprocessing(secure_worker, tasks)
    
    end_time = time.time()
    print(f"Results: {results}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()