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
    max_memory_usage: int = 1024 * 1024 * 1024  # 1GB limit
) -> List[Any]:
    """
    Securely perform parallel processing on a list of data.
    
    Args:
        data: List of items to process
        func: Function to apply to each item
        num_processes: Number of processes to use (default: CPU count)
        max_memory_usage: Maximum allowed memory usage in bytes
    
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
    if num_processes is not None and num_processes <= 0:
        raise ValueError("Number of processes must be positive")
    
    # Set default number of processes
    if num_processes is None:
        num_processes = os.cpu_count()
    
    # Validate max_memory_usage
    if not isinstance(max_memory_usage, int) or max_memory_usage <= 0:
        raise ValueError("Memory usage must be a positive integer")
    
    # Create a pool of workers
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Validate memory usage before processing
        if sum(pool._processes[i].taskqueue.qsize() for i in range(num_processes)) > max_memory_usage:
            raise MemoryError("Memory usage exceeds maximum allowed limit")
        
        # Process data in parallel
        try:
            results = pool.map(func, data)
        except Exception as e:
            logger.error(f"Error during parallel processing: {str(e)}")
            raise
            
    return results

def example_function(item: Any) -> Any:
    """
    Example function to process data items.
    Replace this with your actual processing logic.
    """
    # Simple example: square the input
    return item * item

if __name__ == "__main__":
    # Example usage
    data = list(range(1000))
    results = secure_parallel_process(data, example_function)
    logger.info(f"Processed {len(results)} items")