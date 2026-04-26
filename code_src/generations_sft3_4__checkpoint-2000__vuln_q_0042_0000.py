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
    if num_processes is None or num_processes < 1:
        num_processes = 1
    
    # Validate number of processes
    if num_processes > multiprocessing.cpu_count():
        logger.warning(f"Requested {num_processes} processes, limiting to {multiprocessing.cpu_count()}")
        num_processes = multiprocessing.cpu_count()
    
    # Create secure partial function with limited arguments
    safe_func = partial(func, data=data)
    
    try:
        # Use ProcessPoolExecutor for controlled parallelism
        with multiprocessing.get_context('spawn').Pool(processes=num_processes) as pool:
            # Process data in chunks to prevent memory issues
            chunk_size = max(1, len(data) // num_processes)
            results = []
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i+chunk_size]
                results.extend(pool.map(safe_func, chunk))
        return results
    
    except Exception as e:
        logger.error(f"Error during parallel processing: {str(e)}")
        raise

# Example usage
def example_process(item: Any) -> Any:
    """Example function to process data"""
    return item * 2

if __name__ == "__main__":
    # Example data
    data = list(range(1000))
    
    # Process data in parallel
    results = secure_parallel_process(data, example_process)
    
    # Verify results
    assert all(result > 0 for result in results)
    logger.info(f"Successfully processed {len(results)} items")