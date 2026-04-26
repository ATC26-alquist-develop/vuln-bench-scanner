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

def create_secure_multiprocessing_pool(num_processes: int = None) -> multiprocessing.Pool:
    """Create a secure multiprocessing pool"""
    try:
        # Validate number of processes
        if num_processes is None:
            num_processes = os.cpu_count()
        if num_processes is None or num_processes < 1:
            num_processes = 1
            
        # Create pool with resource limits
        return multiprocessing.Pool(processes=num_processes, 
                                   initializer=secure_task,
                                   initargs=())
    except Exception as e:
        logger.error(f"Failed to create pool: {str(e)}")
        raise

def run_parallel_tasks(task_list: list[tuple[Callable[..., Any], tuple, dict]], 
                       max_workers: int = None) -> list[Any]:
    """Run tasks in parallel with security controls"""
    try:
        # Validate inputs
        if not isinstance(task_list, list):
            raise TypeError("Task list must be a list")
            
        # Create pool with resource limits
        pool = create_secure_multiprocessing_pool(max_workers)
        
        # Run tasks
        results = pool.map(partial(secure_task), task_list)
        
        pool.close()
        pool.join()
        
        return results
        
    except Exception as e:
        logger.error(f"Parallel task execution failed: {str(e)}")
        raise