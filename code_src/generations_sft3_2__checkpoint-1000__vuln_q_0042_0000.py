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
    num_processes: int = os.cpu_count(),
    max_queue_size: int = 1000
) -> List[Any]:
    """
    Securely perform parallel processing on a list of data.
    
    Args:
        data: List of items to process
        func: Function to apply to each item
        num_processes: Number of processes to use (default: CPU count)
        max_queue_size: Maximum queue size to prevent memory issues
    
    Returns:
        List of results from processing
    """
    # Validate inputs
    if not isinstance(data, list):
        raise TypeError("Input data must be a list")
    if not callable(func):
        raise TypeError("Function must be callable")
    if num_processes is None or num_processes <= 0:
        raise ValueError("Number of processes must be positive")
    if max_queue_size <= 0:
        raise ValueError("Max queue size must be positive")

    # Create a secure queue for inter-process communication
    result_queue = multiprocessing.Queue(maxsize=max_queue_size)
    
    # Create a secure function wrapper
    def secure_worker(item):
        try:
            return func(item)
        except Exception as e:
            logger.error(f"Error processing item: {item}. Error: {str(e)}")
            return None

    # Create a secure pool of workers
    with multiprocessing.Pool(
        processes=num_processes,
        initializer=secure_worker,
        maxtasksperchild=1
    ) as pool:
        
        # Process items in parallel
        results = pool.map(partial(secure_worker), data)
        
        # Collect results
        processed_results = []
        while True:
            try:
                result = result_queue.get(timeout=1)
                if result is None:
                    break
                processed_results.append(result)
            except multiprocessing.queues.Empty:
                continue

    return processed_results

# Example usage
def example_function(x: int) -> int:
    """Example function to process data"""
    return x * 2

if __name__ == "__main__":
    # Example data
    data = list(range(1000))
    
    # Perform parallel processing
    results = secure_parallel_process(
        data,
        example_function,
        num_processes=4
    )
    
    logger.info(f"Processed {len(results)} items")