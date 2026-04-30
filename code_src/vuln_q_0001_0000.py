import multiprocessing
import os
import logging
from typing import Callable, List, Any
from functools import partial

# Configure logging securely
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='secure_multiprocessing.log',
    filemode='a'
)

def secure_task(task_func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """
    Secure wrapper for tasks to be run in parallel.
    Limits resource usage and implements proper error handling.
    """
    try:
        # Limit maximum number of processes to prevent resource exhaustion
        max_processes = min(multiprocessing.cpu_count(), 4)
        with multiprocessing.Pool(processes=max_processes) as pool:
            result = pool.apply_async(task_func, args=args, kwds=kwargs)
            return result.get(timeout=30)  # 30 second timeout
    except multiprocessing.TimeoutError:
        logging.error("Task timed out")
        raise
    except Exception as e:
        logging.error(f"Error in task: {str(e)}")
        raise

def run_parallel_tasks(tasks: List[Callable[..., Any]], *args: Any, **kwargs: Any) -> List[Any]:
    """
    Run multiple tasks in parallel with proper resource management.
    """
    if not tasks:
        return []
    
    # Validate task functions
    for task in tasks:
        if not callable(task):
            raise ValueError("All tasks must be callable functions")
    
    # Run tasks securely
    return [secure_task(task, *args, **kwargs) for task in tasks]

# Example usage
def example_task(x: int) -> int:
    """Example task function"""
    return x * 2

if __name__ == '__main__':
    # Run tasks in parallel
    results = run_parallel_tasks([example_task] * 5, 1)
    print(results)