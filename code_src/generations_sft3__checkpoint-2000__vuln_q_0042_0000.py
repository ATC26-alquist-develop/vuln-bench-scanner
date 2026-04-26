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
        data: List of items to process
        func: Function to apply to each item
        num_processes: Number of processes to use (default: CPU count)
    
    Returns:
        List of processed results
    """
    # Validate inputs
    if not isinstance(data, list) or not data:
        raise ValueError("Data must be a non-empty list")
    
    if not callable(func):
        raise ValueError("Function must be callable")
    
    # Set number of processes safely
    if num_processes is None:
        num_processes = os.cpu_count()
    elif not isinstance(num_processes, int) or num_processes <= 0:
        raise ValueError("Number of processes must be a positive integer")
    
    # Validate data size
    if len(data) > 1000000:  # Reasonable limit for large datasets
        raise ValueError("Data size exceeds security limits")
    
    # Create secure partial function
    secure_func = partial(func, _data=data)
    
    try:
        # Use multiprocessing with proper error handling
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.map(secure_func, data)
        return results
        
    except Exception as e:
        logger.error(f"Error during parallel processing: {str(e)}")
        raise

# Example usage
def example_process(item: Any) -> Any:
    """Example function to process data"""
    return item * 2

if __name__ == "__main__":
    # Example of running parallel processing
    try:
        data = list(range(1000000))  # Large dataset
        results = secure_parallel_process(data, example_process)
        logger.info(f"Processed {len(results)} items")
    except Exception as e:
        logger.error(f"Failed to process data: {str(e)}")