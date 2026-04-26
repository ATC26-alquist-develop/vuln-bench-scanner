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
        data: List of data items to process
        func: Function to apply to each item
        num_processes: Number of processes to use (default: CPU count)
        max_memory_mb: Maximum allowed memory usage per process in MB
    
    Returns:
        List of processed results
    """
    # Validate inputs
    if not isinstance(data, list) or not data:
        raise ValueError("Data must be a non-empty list")
    if not callable(func):
        raise ValueError("func must be a callable")
    
    # Set number of processes safely
    if num_processes is None:
        num_processes = os.cpu_count()
    num_processes = max(1, min(num_processes, os.cpu_count()))
    
    # Validate max_memory_mb
    if not isinstance(max_memory_mb, int) or max_memory_mb <= 0:
        raise ValueError("max_memory_mb must be a positive integer")
    
    # Create a secure pool with resource limits
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(processes=num_processes, maxtasksperchild=1) as pool:
        # Use partial to avoid global state
        safe_func = partial(func)
        
        # Process data in chunks to manage memory
        chunk_size = max(1, len(data) // num_processes)
        results = []
        
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            chunk_results = pool.map(safe_func, chunk)
            results.extend(chunk_results)
            
            # Check memory usage periodically
            pool.close()
            pool.join()
            pool = ctx.Pool(processes=num_processes)
            
            # Check memory usage
            mem_usage = ctx.ProcessPoolExecutor().submit(
                _get_memory_usage, 
                pool._processes
            ).result()
            if sum(usage for _, usage in mem_usage.values()) > max_memory_mb:
                logger.warning(f"Memory usage limit reached. Reducing chunk size.")
                chunk_size = max(1, chunk_size // 2)
                pool.close()
                pool.join()
                pool = ctx.Pool(processes=num_processes)
        
        return results

def _get_memory_usage(processes):
    """Safely get memory usage of processes."""
    return {
        p.pid: p.memory_info().rss / (1024 * 1024)  # Convert to MB
        for p in processes
    }

# Example usage
if __name__ == "__main__":
    def example_func(x):
        return x * 2
    
    data = list(range(10000))
    results = secure_parallel_process(data, example_func)
    logger.info(f"Processed {len(results)} items")