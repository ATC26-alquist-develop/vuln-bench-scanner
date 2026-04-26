import multiprocessing
from typing import List, Callable
import os
import logging
from functools import partial

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_worker(func: Callable, data: List, result_queue: multiprocessing.Queue) -> None:
    """Secure worker function for parallel processing"""
    try:
        result = func(data)
        result_queue.put(result)
    except Exception as e:
        logger.error(f"Error in worker: {str(e)}")
        result_queue.put(None)

def secure_parallel_process(
    func: Callable,
    data_chunks: List[List],
    num_processes: int = None
) -> List:
    """
    Secure parallel processing function with safety measures
    
    Args:
        func: Function to apply to each data chunk
        data_chunks: List of data chunks to process
        num_processes: Number of processes to use (default: number of CPU cores)
    
    Returns:
        List of results from parallel processing
    """
    # Validate inputs
    if not callable(func):
        raise ValueError("Function must be callable")
    if not isinstance(data_chunks, list) or not all(isinstance(chunk, list) for chunk in data_chunks):
        raise ValueError("Data must be a list of lists")
    if num_processes is not None and (not isinstance(num_processes, int) or num_processes <= 0):
        raise ValueError("Number of processes must be a positive integer")

    # Determine number of processes
    if num_processes is None:
        num_processes = min(multiprocessing.cpu_count(), len(data_chunks))

    # Create a secure queue for results
    result_queue = multiprocessing.Queue()

    # Create and start processes
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=secure_worker, args=(func, data_chunks[_], result_queue))
        processes.append(p)
        p.start()

    # Collect results
    results = []
    for _ in range(num_processes):
        result = result_queue.get()
        if result is not None:
            results.append(result)
        else:
            logger.warning("Worker returned None, skipping result")

    # Wait for all processes to complete
    for p in processes:
        p.join()

    return results

# Example usage
def example_function(data):
    """Example function to process data"""
    return sum(data)

if __name__ == "__main__":
    # Example data
    large_dataset = list(range(1000000))
    chunk_size = 10000
    data_chunks = [large_dataset[i:i+chunk_size] for i in range(0, len(large_dataset), chunk_size)]

    # Process data in parallel
    results = secure_parallel_process(example_function, data_chunks)

    # Combine results
    final_result = sum(results)
    logger.info(f"Final result: {final_result}")