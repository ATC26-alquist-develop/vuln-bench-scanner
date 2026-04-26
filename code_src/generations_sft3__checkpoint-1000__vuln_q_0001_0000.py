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
        return result
        
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}")
        raise

def secure_multiprocessing(
    task_list: List[Callable[..., Any]],
    num_processes: int = None,
    timeout: int = 30
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
            
    # Create a pool of processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        try:
            # Execute tasks securely
            results = pool.map(
                partial(secure_task),
                task_list
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error in multiprocessing: {str(e)}")
            raise
            
        finally:
            # Ensure proper cleanup
            pool.close()
            pool.join()

# Example usage
if __name__ == "__main__":
    def example_task(x: int) -> int:
        return x * 2
    
    try:
        results = secure_multiprocessing(
            task_list=[example_task for _ in range(5)],
            num_processes=os.cpu_count()
        )
        logger.info(f"Results: {results}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")