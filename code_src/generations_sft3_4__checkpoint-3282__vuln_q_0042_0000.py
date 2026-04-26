import multiprocessing as mp
from typing import List, Any
import os
import signal
from functools import partial

def secure_worker(func: callable, data: Any, worker_id: int) -> Any:
    """Secure worker function with proper error handling and resource management."""
    try:
        # Set resource limits
        resource_limits()
        
        # Set up signal handler
        signal_handler = lambda sig, frame: None
        signal.signal(signal.SIGINT, signal_handler)
        
        # Execute function with error handling
        result = func(data)
        return result, worker_id
        
    except Exception as e:
        return str(e), worker_id

def resource_limits():
    """Set resource limits to prevent resource exhaustion."""
    # Set CPU time limit
    mp.set_start_method('spawn')
    mp.set_resource_limit((180, 180))  # 3 minutes CPU time, 3 minutes wall time

def parallel_process(
    data: List[Any],
    func: callable,
    num_processes: int = None
) -> List[tuple]:
    """
    Perform parallel processing on data using multiprocessing.
    
    Args:
        data: List of data items to process
        func: Function to apply to each data item
        num_processes: Number of processes to use (default: number of CPU cores)
    
    Returns:
        List of tuples containing (result, worker_id) for each item
    """
    # Validate inputs
    if not isinstance(data, list) or not data:
        raise ValueError("Data must be a non-empty list")
    if not callable(func):
        raise ValueError("func must be a callable")
    
    # Determine number of processes
    if num_processes is None:
        num_processes = os.cpu_count()
    if not isinstance(num_processes, int) or num_processes <= 0:
        raise ValueError("num_processes must be a positive integer")
    
    # Create pool with resource limits
    with mp.Pool(processes=num_processes, initializer=resource_limits) as pool:
        # Create partial function with worker
        partial_worker = partial(secure_worker, func)
        
        # Process data in chunks
        chunk_size = max(1, len(data) // num_processes)
        results = []
        
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            partial_results = pool.map_async(partial_worker, chunk)
            partial_results.wait()
            results.extend(partial_results.get())
            
        return results

# Example usage
def example_function(x: int) -> int:
    """Example function to process data"""
    return x * 2

if __name__ == "__main__":
    # Example data
    data = list(range(100))
    
    # Run parallel processing
    results = parallel_process(data, example_function)
    
    # Process results
    for result, worker_id in results:
        print(f"Worker {worker_id}: {result}")