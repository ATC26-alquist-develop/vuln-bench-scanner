import multiprocessing
import os
import logging
from typing import Callable, List, Any
from functools import partial

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_task(task_func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """
    Secure wrapper for task execution with proper error handling and logging.
    """
    try:
        # Validate inputs
        if not callable(task_func):
            raise TypeError("Task function must be callable")
            
        # Execute task with proper error handling
        result = task_func(*args, **kwargs)
        logger.info(f"Task completed successfully: {task_func.__name__}")
        return result
        
    except Exception as e:
        logger.error(f"Error executing task {task_func.__name__}: {str(e)}")
        raise

def secure_multiprocessing(
    task_list: List[Callable[..., Any]],
    num_processes: int = None,
    max_queue_size: int = 100
) -> List[Any]:
    """
    Secure multiprocessing function with proper error handling and resource management.
    """
    # Validate inputs
    if not isinstance(task_list, list) or not task_list:
        raise ValueError("Task list must be a non-empty list")
    
    if num_processes is not None:
        if not isinstance(num_processes, int) or num_processes <= 0:
            raise ValueError("Number of processes must be a positive integer")
            
    # Create process pool with proper resource limits
    with multiprocessing.Pool(
        processes=num_processes,
        initializer=multiprocessing.set_start_method,
        initargs=(multiprocessing.get_context('spawn'),),
        maxtasksperchild=1,
        max_queue_size=max_queue_size
    ) as pool:
        
        # Execute tasks in parallel
        results = pool.map(
            secure_task,
            task_list
        )
        
        return results

# Example usage
if __name__ == "__main__":
    def example_task(x: int) -> int:
        return x * 2
    
    # Create a list of tasks
    tasks = [partial(example_task, x) for x in range(10)]
    
    # Run tasks in parallel
    results = secure_multiprocessing(tasks)
    
    # Process results
    for i, result in enumerate(results):
        print(f"Result {i}: {result}")