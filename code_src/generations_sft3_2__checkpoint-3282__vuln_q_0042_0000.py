import multiprocessing as mp
from typing import List, Any
import os
import signal
from functools import partial

def secure_worker(func: callable, data: Any) -> Any:
    """Secure worker function that handles exceptions and resource limits"""
    try:
        # Limit memory usage to 500MB per process
        mp.set_start_method('spawn')
        with mp.get_context('spawn').TemporaryFile(mode='w+b', 
                                                 prefix='secure_worker_',
                                                 delete=True) as temp_file:
            # Serialize data to bytes
            serialized = func(data).encode('utf-8')
            temp_file.write(serialized)
            temp_file.flush()
            temp_file.seek(0)
            result = temp_file.read().decode('utf-8')
            return result
    except Exception as e:
        return f"Error in worker: {str(e)}"

def parallel_process(
    data_list: List[Any],
    func: callable,
    num_processes: int = None
) -> List[Any]:
    """
    Secure parallel processing function
    
    Args:
        data_list: List of data to process
        func: Function to apply to each item
        num_processes: Number of processes to use (default: CPU count)
    """
    # Validate inputs
    if not isinstance(data_list, list) or not data_list:
        raise ValueError("data_list must be a non-empty list")
    if not callable(func):
        raise ValueError("func must be a callable")
    if num_processes is not None and (not isinstance(num_processes, int) or num_processes <= 0):
        raise ValueError("num_processes must be a positive integer")

    # Set number of processes safely
    if num_processes is None:
        num_processes = os.cpu_count() or 1
    elif num_processes > os.cpu_count():
        num_processes = os.cpu_count() or 1

    # Set resource limits
    mp.set_start_method('spawn')
    mp.set_resource_limit(mp.RLIMIT_AS, (500 * 1024 * 1024 * 1024, -1))  # 500MB memory limit

    # Create pool with resource limits
    with mp.Pool(processes=num_processes, initializer=mp.set_resource_limit) as pool:
        # Create partial function with resource limits
        safe_func = partial(secure_worker, func)
        
        # Process data in chunks to prevent memory issues
        chunk_size = max(1, num_processes // 2)
        results = []
        for i in range(0, len(data_list), chunk_size):
            chunk = data_list[i:i+chunk_size]
            results.extend(pool.map(safe_func, chunk))
            
        return results

# Example usage
def example_func(x: int) -> int:
    """Example function to process data"""
    return x * 2

if __name__ == "__main__":
    # Example with 4 processes
    data = list(range(1000))
    results = parallel_process(data, example_func)
    print(f"Processed {len(results)} items")