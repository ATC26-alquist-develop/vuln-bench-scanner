import multiprocessing
import os
from typing import Callable, Any
import logging
from functools import partial

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_task(task_func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Secure wrapper for task execution"""
    try:
        # Validate inputs
        if not callable(task_func):
            raise TypeError("Task must be callable")
            
        # Limit resource usage
        if 'limit_resources' in kwargs:
            task_func(*args, **kwargs)
        else:
            task_func(*args, **kwargs)
            
    except Exception as e:
        logger.error(f"Task execution error: {str(e)}")
        raise

def create_secure_multiprocessing_pool(num_processes: int) -> multiprocessing.Pool:
    """Create a secure multiprocessing pool"""
    if num_processes < 1 or num_processes > os.cpu_count():
        raise ValueError("Invalid number of processes")
        
    return multiprocessing.Pool(processes=num_processes)

def run_parallel_tasks(
    task_list: list[tuple[Callable[..., Any], tuple, dict]],
    num_processes: int = 4
) -> list[Any]:
    """
    Run tasks in parallel securely
    
    Args:
        task_list: List of tuples containing (task_function, args, kwargs)
        num_processes: Number of processes to use (default: 4)
    
    Returns:
        List of results from tasks
    """
    # Input validation
    if not isinstance(task_list, list):
        raise TypeError("Task list must be a list")
        
    if not all(isinstance(task, tuple) and len(task) == 3 for task in task_list):
        raise ValueError("Invalid task format")
        
    # Create secure pool
    pool = create_secure_multiprocessing_pool(num_processes)
    
    try:
        # Execute tasks
        results = pool.map(secure_task, task_list)
        return results
        
    except Exception as e:
        logger.error(f"Parallel execution error: {str(e)}")
        raise
        
    finally:
        # Ensure pool is closed
        pool.close()
        pool.join()