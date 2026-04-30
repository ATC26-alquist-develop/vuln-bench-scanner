```python
import multiprocessing
from typing import List, Callable, Any
import os
import logging
from functools import partial

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def secure_worker(func: Callable, data: Any, max_size: int = 1024 * 1024 * 100) -> Any:
    """
    Secure worker function for multiprocessing.
    Validates input size and type before processing.
    """
    if not callable(func):
        raise TypeError("Function must be callable")
    if not isinstance(data, (list, tuple, set, dict)):
        raise TypeError("Data must be a list, tuple, set, or dict")
    if len(str(data)) > max_size:
        raise ValueError("Data size exceeds maximum allowed size")
    return func(data)

def parallel_process(data: List[Any], func: Callable, num_processes: int = None) -> List[Any]:
    """
    Secure parallel processing function.
    Uses multiprocessing with proper resource management.
    """
    if not callable(func):
        raise TypeError("Function must be callable")
    if not isinstance(data, list):
        raise TypeError("Data must be a list")
    if num_processes is not None and not isinstance(num_processes, int) or num_processes <= 0:
        raise ValueError("Number of processes must be a positive integer")
    
    try:
        # Determine number of processes
        if num_processes is None:
            num_processes = min(multiprocessing.cpu_count(), len(data))
        
        # Create a pool of workers with resource limits
        with multiprocessing.Pool(processes=num_processes, 
                                 maxtasksperchild=1000, 
                                 initializer=partial(os.setenv, 'MKL_NUM_THREADS', '1')) as pool:
            # Process data in chunks to prevent memory issues
            chunk_size = max(1, len(data) // num_processes)
            results = []
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i+chunk_size]
                results.extend(pool.map(partial(secure_worker, func, max_size=1024 * 1024 * 100), chunk))
            return results
    except Exception as e:
        logging.error(f"Error during parallel processing: {str(e)}")
        raise
```