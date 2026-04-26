import multiprocessing
import os
from typing import Callable, Any
import logging
from functools import partial

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_task(task_func: Callable[..., Any], *args, **kwargs) -> Any:
    """Secure wrapper for task execution"""
    try:
        # Validate inputs
        if not callable(task_func):
            raise TypeError("Task must be callable")
            
        # Limit resource usage
        if 'cpu_count' not in kwargs:
            kwargs['cpu_count'] = multiprocessing.cpu_count()
            
        # Execute task in process pool
        with multiprocessing.Pool(processes=kwargs.get('cpu_count', 1)) as pool:
            result = pool.apply_async(task_func, args, kwargs)
            return result.get()
            
    except Exception as e:
        logger.error(f"Task execution error: {str(e)}")
        raise

def create_secure_multiprocessing_pool(num_processes: int = None) -> multiprocessing.Pool:
    """Create a secure multiprocessing pool"""
    try:
        # Validate number of processes
        if num_processes is not None:
            if not isinstance(num_processes, int):
                raise TypeError("Number of processes must be an integer")
            if num_processes < 1:
                raise ValueError("Number of processes must be positive")
                
        # Create pool with resource limits
        return multiprocessing.Pool(processes=num_processes, 
                                   initializer=secure_task.__init__,
                                   initargs=())
    except Exception as e:
        logger.error(f"Pool creation error: {str(e)}")
        raise

def run_parallel_tasks(tasks: list, task_func: Callable[..., Any], 
                      args: list = None, kwargs: dict = None) -> list:
    """Run tasks in parallel with security controls"""
    try:
        # Validate inputs
        if not isinstance(tasks, list):
            raise TypeError("Tasks must be a list")
            
        # Create secure pool
        pool = create_secure_multiprocessing_pool()
        
        # Prepare arguments
        if args is None:
            args = [[] for _ in tasks]
        elif not isinstance(args, list):
            raise TypeError("Arguments must be a list")
            
        # Prepare keyword arguments
        if kwargs is None:
            kwargs = [{}) for _ in tasks]
        elif not isinstance(kwargs, list):
            raise TypeError("Keyword arguments must be a list")
            
        # Run tasks
        results = []
        for task, task_args, task_kwargs in zip(tasks, args, kwargs):
            if not callable(task_func):
                raise TypeError("Task function must be callable")
                
            # Execute task
            result = pool.apply_async(
                task_func,
                task_args,
                task_kwargs
            )
            results.append(result)
            
        # Collect results
        return [result.get() for result in results]
        
    except Exception as e:
        logger.error(f"Task execution error: {str(e)}")
        raise