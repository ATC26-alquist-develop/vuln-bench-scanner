import multiprocessing
from typing import List, Callable
import os
import logging
from functools import partial

def secure_multiprocessing(func: Callable, 
                          data: List, 
                          num_processes: int = None) -> List:
    """
    Securely perform parallel computations using multiprocessing.
    
    Args:
        func: Callable function to apply to each data item
        data: List of data items to process
        num_processes: Number of processes to use (defaults to number of CPU cores)
    
    Returns:
        List of results from parallel computation
        
    Raises:
        ValueError: If inputs are invalid
        RuntimeError: If multiprocessing fails
    """
    # Input validation
    if not callable(func):
        raise ValueError("Function must be callable")
    if not isinstance(data, list):
        raise ValueError("Data must be a list")
    if not data:
        raise ValueError("Data list cannot be empty")
    if num_processes is not None and not isinstance(num_processes, int):
        raise ValueError("Number of processes must be an integer")
        
    # Determine number of processes
    if num_processes is None:
        num_processes = min(multiprocessing.cpu_count(), len(data))
        
    # Validate number of processes
    if num_processes <= 0 or num_processes > len(data):
        raise ValueError("Invalid number of processes")
        
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Create pool with context manager
        with multiprocessing.Pool(processes=num_processes) as pool:
            # Use partial to pass additional arguments
            func_with_args = partial(func)
            
            # Process data in parallel
            results = pool.map(func_with_args, data)
            
        return results
        
    except Exception as e:
        logger.error(f"Multiprocessing error: {str(e)}")
        raise RuntimeError("Multiprocessing failed") from e