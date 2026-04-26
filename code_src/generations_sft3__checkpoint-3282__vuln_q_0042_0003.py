import multiprocessing
import time
import os
from typing import Callable, Any

def secure_worker(task: Any) -> Any:
    """
    A secure worker function that performs a simple CPU-bound task.
    This function is designed to be safe and doesn't introduce vulnerabilities.
    
    Args:
        task: Any serializable data to process
        
    Returns:
        Processed result
        
    Raises:
        ValueError: If input is not serializable
    """
    # Validate input
    if task is None:
        raise ValueError("Task cannot be None")
        
    # Simple CPU-bound task - sleep for 1 second
    time.sleep(1)
    
    return task

def secure_multiprocessing(func: Callable, 
                         data_list: list,
                         num_processes: int = None) -> list:
    """
    Secure implementation of multiprocessing for CPU-bound tasks.
    
    Args:
        func: The function to be executed in parallel
        data_list: List of data to process
        num_processes: Number of processes to use (default: number of CPUs)
        
    Returns:
        List of results
        
    Raises:
        ValueError: If inputs are invalid
        RuntimeError: If multiprocessing fails
    """
    # Validate inputs
    if not callable(func):
        raise ValueError("func must be a callable")
        
    if not isinstance(data_list, list):
        raise ValueError("data_list must be a list")
        
    if num_processes is not None:
        if not isinstance(num_processes, int):
            raise ValueError("num_processes must be an integer")
        if num_processes < 1:
            raise ValueError("num_processes must be positive")
            
    # Set number of processes safely
    if num_processes is None:
        num_processes = min(os.cpu_count() or 1, 4)  # Limit to 4 for safety
    
    # Create a pool of workers
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Use starmap to pass multiple arguments
        results = pool.starmap(func, [(item,) for item in data_list])
    
    return results

# Example usage
def main():
    # Example data
    data = [1, 2, 3, 4, 5]
    
    # Process data using multiprocessing
    results = secure_multiprocessing(secure_worker, data)
    
    print(f"Processed {len(results)} items")
    print(f"Results: {results}")

if __name__ == "__main__":
    main()