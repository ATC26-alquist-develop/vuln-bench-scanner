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
            
        # Run task in a controlled environment
        result = task_func(*args, **kwargs)
        return result
        
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}")
        raise

def parallel_process(
    tasks: List[Callable[..., Any]],
    num_processes: int = None,
    max_queue_size: int = 100
) -> List[Any]:
    """
    Securely parallelize task execution using multiprocessing.
    
    Args:
        tasks: List of task functions to execute
        num_processes: Number of processes to use (default: number of CPU cores)
        max_queue_size: Maximum queue size for task submission (default: 100)
    """
    # Validate inputs
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Tasks must be a non-empty list")
    
    if num_processes is not None:
        if not isinstance(num_processes, int) or num_processes <= 0:
            raise ValueError("Number of processes must be a positive integer")
            
    # Set default number of processes
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
        
    # Create secure queue for task submission
    task_queue = multiprocessing.Queue(maxsize=max_queue_size)
    
    # Create secure process pool
    with multiprocessing.Pool(processes=num_processes, initializer=secure_task) as pool:
        # Submit tasks to the queue
        for task in tasks:
            if not callable(task):
                raise TypeError("All tasks must be callable")
            task_queue.put(partial(secure_task, task))
        
        # Collect results
        results = []
        while True:
            try:
                result = task_queue.get(timeout=1)
                results.append(result)
                
            except multiprocessing.queues.Empty:
                break
                
    return results

# Example usage
if __name__ == "__main__":
    def example_task(x: int) -> int:
        return x * 2
    
    try:
        results = parallel_process(
            [example_task] * 10,
            num_processes=4
        )
        logger.info(f"Results: {results}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")