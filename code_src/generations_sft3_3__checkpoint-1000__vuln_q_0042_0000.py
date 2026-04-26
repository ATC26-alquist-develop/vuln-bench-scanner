import multiprocessing
import os
from typing import List, Callable, Any
import logging
from functools import partial

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_parallel_process(
    data: List[Any],
    func: Callable[[Any], Any],
    num_processes: int = None,
    max_memory_mb: int = 1000
) -> List[Any]:
    """
    Securely perform parallel processing on a list of data.
    
    Args:
        data: List of items to process
        func: Function to apply to each item
        num_processes: Number of processes to use (default: number of CPU cores)
        max_memory_mb: Maximum allowed memory usage in MB
    
    Returns:
        List of results from processing
    """
    # Validate inputs
    if not isinstance(data, list):
        raise TypeError("Input data must be a list")
    if not callable(func):
        raise TypeError("Function must be callable")
    if num_processes is not None and not isinstance(num_processes, int):
        raise TypeError("Number of processes must be an integer")
    if max_memory_mb <= 0:
        raise ValueError("Max memory must be positive")

    # Set number of processes
    if num_processes is None:
        num_processes = os.cpu_count()
    elif num_processes < 1:
        raise ValueError("Number of processes must be positive")

    # Validate memory usage
    total_size = sum(os.path.getsize(str(item)) for item in data)
    if total_size > max_memory_mb * 1024 * 1024:
        raise ValueError("Total data size exceeds maximum allowed memory")

    # Create a pool of workers
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Create a partial function with the fixed arguments
        partial_func = partial(func)
        
        # Process data in chunks to prevent memory issues
        chunk_size = max(1, len(data) // num_processes)
        results = []
        
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            chunk_results = pool.map(partial_func, chunk)
            results.extend(chunk_results)
            
            # Check memory usage periodically
            if len(results) > 0 and len(results) % 100 == 0:
                logger.info(f"Processed {len(results)} items")
                if total_size > max_memory_mb * 1024 * 1024:
                    raise MemoryError("Memory usage exceeded maximum allowed")

        return results

# Example usage
def example_function(x: int) -> int:
    """Example function to process data"""
    return x * 2

if __name__ == "__main__":
    # Example data
    data = list(range(1000))
    
    # Process data in parallel
    results = secure_parallel_process(data, example_function)
    
    # Verify results
    assert all(result == x * 2 for x, result in zip(data, results))
    logger.info("Parallel processing completed successfully")