import multiprocessing
import time
import os
from typing import Callable, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_task(task_id: int, duration: int) -> None:
    """Secure task function that performs a simple CPU-bound operation."""
    logger.info(f"Task {task_id} started")
    try:
        # Simulate work with a CPU-bound operation
        start_time = time.time()
        while time.time() - start_time < duration:
            _ = [x**2 for x in range(1000000)]
    except Exception as e:
        logger.error(f"Error in task {task_id}: {str(e)}")
    finally:
        logger.info(f"Task {task_id} completed")

def create_secure_multiprocessing_pool(num_processes: int = None) -> tuple:
    """
    Creates a secure multiprocessing pool with proper resource management.
    
    Args:
        num_processes: Number of worker processes. If None, uses number of CPUs.
    
    Returns:
        tuple: (Pool, Lock) for proper cleanup
    """
    try:
        # Validate inputs
        if num_processes is not None and (not isinstance(num_processes, int) or num_processes <= 0):
            raise ValueError("Number of processes must be a positive integer or None")
        
        # Create pool with proper resource limits
        pool = multiprocessing.Pool(processes=num_processes, 
                                   initializer=_init_worker,
                                   initargs=())
        
        # Create a lock for synchronization
        lock = multiprocessing.Lock()
        
        return pool, lock
    
    except Exception as e:
        logger.error(f"Error creating multiprocessing pool: {str(e)}")
        raise

def _init_worker(lock: multiprocessing.Lock) -> None:
    """Worker initialization function for proper cleanup."""
    global worker_lock
    worker_lock = lock

def secure_multiprocessing_task(tasks: list[tuple[int, int]]) -> None:
    """
    Securely runs multiple tasks in parallel using multiprocessing.
    
    Args:
        tasks: List of tuples containing (task_id, duration)
    """
    try:
        # Create secure pool with proper cleanup
        pool, lock = create_secure_multiprocessing_pool()
        
        # Validate input
        if not isinstance(tasks, list) or not all(isinstance(t, tuple) and len(t) == 2 
                                                 for t in tasks):
            raise ValueError("Invalid task format")
            
        # Run tasks in parallel with proper synchronization
        results = pool.starmap(secure_task, tasks, 
                              chunksize=1)  # Use chunksize=1 for better control
        
        # Wait for all tasks to complete
        pool.close()
        pool.join()
        
        # Clean up
        del pool
        del lock
        
        logger.info("All tasks completed successfully")
        
    except Exception as e:
        logger.error(f"Error in secure multiprocessing task: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        tasks = [(i, 5) for i in range(10)]
        secure_multiprocessing_task(tasks)
    except Exception as e:
        logger.error(f"Main execution error: {str(e)}")