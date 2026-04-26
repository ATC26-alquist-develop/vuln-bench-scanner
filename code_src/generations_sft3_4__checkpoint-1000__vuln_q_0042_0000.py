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
        data: List of data items to process
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
        raise ValueError("Maximum memory must be positive")

    # Set number of processes
    if num_processes is None:
        num_processes = os.cpu_count()
    elif num_processes < 1:
        raise ValueError("Number of processes must be positive")

    # Validate memory usage
    total_size = sum(os.path.getsize(str(item)) for item in data)
    if total_size > max_memory_mb * 1024 * 1024:
        raise ValueError("Total data size exceeds maximum allowed memory")

    # Create pool with proper resource limits
    with multiprocessing.Pool(processes=num_processes, 
                             initializer=secure_worker_init,
                             initargs=(max_memory_mb,),
                             maxtasksperchild=1) as pool:
        
        # Process data in chunks
        chunk_size = max(1, len(data) // num_processes)
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Process chunks in parallel
        results = []
        for chunk in chunks:
            results.extend(pool.map(func, chunk))
        
        return results

def secure_worker_init(max_memory_mb: int):
    """
    Initialize worker processes with memory limits.
    """
    # Set resource limits
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (max_memory_mb * 1024 * 1024, -1))
    logger.info(f"Worker process initialized with memory limit of {max_memory_mb}MB")

def example_function(x: int) -> int:
    """
    Example function to process data.
    """
    return x * 2

if __name__ == "__main__":
    # Example usage
    data = list(range(1000))
    results = secure_parallel_process(data, example_function)
    logger.info(f"Processed {len(results)} items")