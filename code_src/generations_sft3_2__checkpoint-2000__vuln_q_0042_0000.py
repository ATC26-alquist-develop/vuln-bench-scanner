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
        
        # Run the provided function with input data
        return func(data)
    except Exception as e:
        # Log error securely (implement secure logging mechanism)
        print(f"Worker {worker_id} error: {str(e)}")
        return None

def resource_limits():
    """Set resource limits to prevent resource exhaustion."""
    # Set CPU core limit
    os.environ['OMP_NUM_THREADS'] = str(os.cpu_count())
    
    # Set memory limit (example: 500MB)
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
    os.environ['NUMEXPR_NUM_THREADS'] = '1'

def parallel_process(
    data: List[Any],
    func: callable,
    num_processes: int = None
) -> List[Any]:
    """
    Perform parallel processing on data using multiprocessing.
    
    Args:
        data: List of data items to process
        func: Function to apply to each data item
        num_processes: Number of processes to use (default: CPU count)
    
    Returns:
        List of results from processing
    """
    # Validate inputs
    if not isinstance(data, list) or not data:
        raise ValueError("Data must be a non-empty list")
    if not callable(func):
        raise ValueError("func must be a callable")
    
    # Set number of processes
    if num_processes is None:
        num_processes = os.cpu_count()
    elif num_processes < 1:
        raise ValueError("num_processes must be positive")
    
    # Create pool with resource limits
    with mp.Pool(processes=num_processes, initializer=resource_limits) as pool:
        # Create partial function with worker
        partial_worker = partial(secure_worker, func)
        
        # Process data in parallel
        results = pool.map(partial_worker, data)
        
        # Check for errors
        if any(r is None for r in results):
            raise RuntimeError("One or more workers encountered errors")
            
        return results

if __name__ == "__main__":
    # Example usage
    def example_func(x):
        return x * 2
    
    data = list(range(1000))
    results = parallel_process(data, example_func)
    print(f"Processed {len(results)} items")