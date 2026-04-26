import multiprocessing
import os
from typing import Callable, Any, List
import logging
from functools import partial

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_parallel_process(
    data: List[Any],
    func: Callable[[Any], Any],
    num_processes: int = None
) -> List[Any]:
    """
    Securely process data in parallel using multiprocessing.
    
    Args:
        data: List of data items to process
        func: Function to apply to each item
        num_processes: Number of processes to use (default: CPU count)
    
    Returns:
        List of processed results
    """
    # Validate inputs
    if not isinstance(data, list):
        raise TypeError("Input data must be a list")
    if not callable(func):
        raise TypeError("Function must be callable")
    if num_processes is not None and not isinstance(num_processes, int):
        raise TypeError("Number of processes must be an integer")
    
    # Set number of processes safely
    if num_processes is None:
        num_processes = os.cpu_count()
    if num_processes is not None and num_processes < 1:
        raise ValueError("Number of processes must be positive")
    
    # Create secure process pool
    try:
        with multiprocessing.Pool(processes=num_processes) as pool:
            # Use partial to avoid global state
            safe_func = partial(func)
            
            # Process data in parallel
            results = pool.map(safe_func, data)
            
            return results
            
    except Exception as e:
        logger.error(f"Error in parallel processing: {str(e)}")
        raise

def example_function(item: int) -> int:
    """
    Example function to process data items.
    """
    return item * 2

if __name__ == "__main__":
    # Example usage
    data = list(range(1000))
    results = secure_parallel_process(data, example_function)
    print(f"Processed {len(results)} items")