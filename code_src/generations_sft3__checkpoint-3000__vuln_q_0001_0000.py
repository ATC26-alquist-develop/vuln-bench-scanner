import multiprocessing
import time
import logging
from typing import Callable, Any
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_task(task_id: int, task_func: Callable[[], Any]) -> None:
    """Secure wrapper for individual tasks"""
    try:
        logger.info(f"Starting task {task_id}")
        task_func()
        logger.info(f"Completed task {task_id}")
    except Exception as e:
        logger.error(f"Error in task {task_id}: {str(e)}")

def create_secure_multiprocessing_pool(num_processes: int) -> multiprocessing.Pool:
    """Create a secure multiprocessing pool"""
    if num_processes < 1 or num_processes > os.cpu_count():
        raise ValueError("Invalid number of processes requested")
    
    return multiprocessing.Pool(processes=num_processes)

def run_parallel_tasks(
    num_tasks: int,
    task_func: Callable[[], Any],
    num_processes: int = 4
) -> None:
    """Run tasks in parallel using multiprocessing"""
    if num_tasks < 1:
        raise ValueError("Number of tasks must be positive")
    
    # Create secure pool with proper resource limits
    pool = create_secure_multiprocessing_pool(num_processes)
    
    try:
        # Use list comprehension with context manager for controlled execution
        results = [
            pool.apply_async(secure_task, (i, task_func))
            for i in range(num_tasks)
        ]
        
        # Wait for all tasks to complete
        for result in results:
            result.get()
            
    except Exception as e:
        logger.error(f"Error in parallel task execution: {str(e)}")
    finally:
        # Ensure proper cleanup
        pool.close()
        pool.join()

# Example usage
if __name__ == "__main__":
    def sample_task():
        time.sleep(1)
        return "Task completed"
    
    run_parallel_tasks(5, sample_task)