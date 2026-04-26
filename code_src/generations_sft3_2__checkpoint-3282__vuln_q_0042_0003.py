import multiprocessing
import time
import os
from typing import Callable, Any

def secure_worker(task: Any) -> Any:
    """
    A secure worker function that performs a simple CPU-bound task.
    This function is designed to be safe and doesn't introduce vulnerabilities.
    
    Args:
        task: Any object that can be safely processed
        
    Returns:
        The result of processing the task
        
    Raises:
        ValueError: If task is not serializable
    """
    # Validate input
    if task is None:
        raise ValueError("Task cannot be None")
        
    # Simple CPU-bound task - sleep for 1 second
    time.sleep(1)
    
    return task

def secure_multiprocessing_task(
    task_list: list,
    num_processes: int = None
) -> list:
    """
    Securely process a list of tasks using multiprocessing.
    
    Args:
        task_list: List of tasks to process
        num_processes: Number of processes to use (default: number of CPU cores)
        
    Returns:
        List of results from processing tasks
        
    Raises:
        ValueError: If num_processes is invalid
    """
    # Validate inputs
    if not isinstance(task_list, list):
        raise ValueError("task_list must be a list")
    if num_processes is not None and not isinstance(num_processes, int):
        raise ValueError("num_processes must be an integer or None")
    if num_processes is not None and num_processes < 1:
        raise ValueError("num_processes must be positive")
        
    # Determine number of processes safely
    if num_processes is None:
        num_processes = min(multiprocessing.cpu_count(), 4)
    elif num_processes > 4:
        num_processes = 4
        
    # Create a pool of workers
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Process tasks using the worker function
        results = pool.map(secure_worker, task_list)
        
    return results

# Example usage
if __name__ == "__main__":
    # Example task list
    tasks = [1, 2, 3, 4, 5]
    
    # Process tasks using multiprocessing
    results = secure_multiprocessing_task(tasks)
    
    print(f"Processed {len(results)} tasks")