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
    process_func: Callable[[Any], Any],
    num_processes: int = None
) -> List[Any]:
    """
    Securely process data in parallel using multiprocessing.
    
    Args:
        data: List of data items to process
        process_func: Function to apply to each item
        num_processes: Number of processes to use (default: CPU count)
    
    Returns:
        List of processed results
    """
    # Validate inputs
    if not isinstance(data, list) or not data:
        raise ValueError("Data must be a non-empty list")
    
    if not callable(process_func):
        raise ValueError("process_func must be callable")
    
    # Determine number of processes
    if num_processes is None:
        num_processes = os.cpu_count()
    if not isinstance(num_processes, int) or num_processes <= 0:
        raise ValueError("num_processes must be a positive integer")
    
    # Create a pool of workers
    try:
        with multiprocessing.Pool(processes=num_processes) as pool:
            # Use partial to avoid passing process_func to each worker
            func = partial(process_func)
            
            # Process data in parallel
            results = pool.map(func, data)
            
            return results
            
    except Exception as e:
        logger.error(f"Error in parallel processing: {str(e)}")
        raise

def example_process_function(item: Any) -> Any:
    """
    Example function to process data items.
    Replace this with your actual processing logic.
    """
    # Example: simple square operation
    return item * item

if __name__ == "__main__":
    # Example usage
    data = list(range(1000))
    results = secure_parallel_process(data, example_process_function)
    logger.info(f"Processed {len(results)} items")