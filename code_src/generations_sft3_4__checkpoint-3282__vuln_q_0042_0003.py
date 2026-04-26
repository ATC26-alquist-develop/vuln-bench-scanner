import multiprocessing
import time
import os
from typing import Callable, Any

def secure_worker(task: Any) -> Any:
    """
    A secure worker function that performs a simple CPU-bound task.
    This function is designed to be safe and doesn't introduce any vulnerabilities.
    
    Args:
        task: Any serializable data to process
        
    Returns:
        Processed result
        
    Raises:
        ValueError: If input is not serializable
    """
    # Validate input
    if not isinstance(task, (int, float, str, bytes, list, dict)):
        raise ValueError("Invalid input type")
        
    # Simple CPU-bound task - sum of numbers
    try:
        result = sum(task)
        return result
    except Exception as e:
        raise ValueError(f"Error processing task: {str(e)}")

def secure_multiprocessing(func: Callable, data: list, num_processes: int = None) -> list:
    """
    Secure implementation of multiprocessing for CPU-bound tasks.
    
    Args:
        func: The function to be executed in parallel
        data: List of data to be processed
        num_processes: Number of processes to spawn (default: number of CPU cores)
        
    Returns:
        List of results
        
    Raises:
        ValueError: If inputs are invalid
    """
    # Validate inputs
    if not callable(func):
        raise ValueError("First argument must be a callable function")
        
    if not isinstance(data, (list, tuple)):
        raise ValueError("Data must be a list or tuple")
        
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
        # Process data in chunks to prevent memory issues
        chunk_size = max(1, len(data) // num_processes)
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Process data in parallel
        results = pool.map(func, chunks)
        
        # Flatten results
        return [item for sublist in results for item in sublist]

# Example usage
if __name__ == "__main__":
    # Example CPU-intensive task - sum of numbers
    def example_task(x):
        return secure_worker(x)
    
    # Test with a list of numbers
    data = list(range(1000000))
    start_time = time.time()
    results = secure_multiprocessing(example_task, data)
    end_time = time.time()
    
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"First 10 results: {results[:10]}")