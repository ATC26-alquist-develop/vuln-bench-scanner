import multiprocessing
from typing import Callable, List, Any
import os
import logging
from functools import partial

def secure_multiprocessing(
    tasks: List[Callable[..., Any]],
    max_workers: int = None,
    timeout: int = 30
) -> List[Any]:
    """
    Securely run multiple tasks in parallel using multiprocessing.
    
    Args:
        tasks: List of callable tasks to execute
        max_workers: Maximum number of worker processes (default: None, uses os.cpu_count())
        timeout: Maximum execution time per task in seconds (default: 30)
    
    Returns:
        List of results from tasks
        
    Raises:
        ValueError: If tasks are invalid or timeout is negative
        RuntimeError: If task execution fails
    """
    # Input validation
    if not tasks or not isinstance(tasks, list):
        raise ValueError("Tasks must be a non-empty list of callable objects")
        
    if max_workers is not None and (not isinstance(max_workers, int) or max_workers <= 0):
        raise ValueError("max_workers must be a positive integer or None")
        
    if timeout < 0:
        raise ValueError("Timeout must be non-negative")

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Create a pool of worker processes
    try:
        with multiprocessing.Pool(
            processes=max_workers or os.cpu_count(),
            initializer=partial(os.environ.get, 'PYTHONPATH'),
            timeout=timeout
        ) as pool:
            # Execute tasks securely
            results = []
            for task in tasks:
                if not callable(task):
                    logger.error(f"Invalid task: {task}")
                    continue
                    
                try:
                    result = pool.apply_async(
                        partial(task),
                        (),  # No arguments to prevent injection
                        timeout=timeout
                    )
                    results.append(result)
                except Exception as e:
                    logger.error(f"Task execution failed: {str(e)}")
                    raise RuntimeError(f"Task execution failed: {str(e)}")
            
            # Collect results
            return [r.get(timeout=timeout) for r in results]
            
    except multiprocessing.TimeoutError:
        logger.error("Task execution timed out")
        raise RuntimeError("Task execution timed out")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise RuntimeError(f"Unexpected error: {str(e)}")