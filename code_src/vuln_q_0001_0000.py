import multiprocessing
from typing import Callable, List
import os
import logging
from functools import partial

def secure_multiprocessing(func: Callable, args_list: List[tuple], max_workers: int = None) -> List:
    """
    Securely run multiple tasks in parallel using multiprocessing.
    
    Args:
        func: Callable function to execute
        args_list: List of argument tuples for each task
        max_workers: Maximum number of worker processes (default: number of CPU cores)
    
    Returns:
        List of results from each task
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Validate input
    if not callable(func):
        raise ValueError("Function must be callable")
    if not isinstance(args_list, list):
        raise ValueError("Arguments must be provided as a list")
    if not all(isinstance(args, tuple) for args in args_list):
        raise ValueError("Each argument must be a tuple")
    if len(args_list) == 0:
        raise ValueError("At least one task must be provided")
    
    # Validate max_workers
    if max_workers is not None:
        if not isinstance(max_workers, int) or max_workers <= 0:
            raise ValueError("max_workers must be a positive integer")
        max_workers = min(max_workers, os.cpu_count() or 1)
    
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=max_workers) as pool:
        try:
            # Execute tasks securely
            results = pool.map(func, args_list)
            logger.info(f"Successfully completed {len(results)} tasks")
            return results
        except Exception as e:
            logger.error(f"Error during task execution: {str(e)}")
            raise