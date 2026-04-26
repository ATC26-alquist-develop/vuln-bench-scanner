import multiprocessing
import os
from typing import List, Any, Callable
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
    Securely process data in parallel using multiprocessing.
    
    Args:
        data: Input data to process
        func: Function to apply to each item
        num_processes: Number of processes to use (default: CPU count)
        max_memory_mb: Maximum allowed memory usage per process in MB
    
    Returns:
        List of processed results
    """
    # Validate inputs
    if not isinstance(data, list):
        raise TypeError("Input data must be a list")
    if not callable(func):
        raise TypeError("Function must be callable")
    if num_processes is not None and not isinstance(num_processes, int):
        raise TypeError("num_processes must be an integer or None")
    if num_processes is not None and num_processes < 1:
        raise ValueError("num_processes must be positive")
    
    # Set number of processes safely
    if num_processes is None:
        num_processes = os.cpu_count() or 1
    num_processes = max(1, min(num_processes, os.cpu_count() or 1))
    
    # Validate max_memory_mb
    if max_memory_mb < 1:
        raise ValueError("max_memory_mb must be positive")
    
    # Create secure process pool
    try:
        with multiprocessing.Pool(processes=num_processes, 
                                 initializer=_init_process,
                                 initargs=(max_memory_mb,)) as pool:
            
            # Process data in chunks to prevent memory issues
            chunk_size = max(1, len(data) // num_processes)
            results = []
            
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i+chunk_size]
                results.extend(pool.map(func, chunk))
            
            return results
            
    except Exception as e:
        logger.error(f"Error in parallel processing: {str(e)}")
        raise

def _init_process(max_memory_mb: int):
    """Initialize each process with memory limits."""
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (max_memory_mb * 1024 * 1024, -1))

# Example usage
if __name__ == "__main__":
    def example_func(x: int) -> int:
        return x * 2
    
    data = list(range(1000))
    results = secure_parallel_process(data, example_func)
    print(f"Processed {len(results)} items")