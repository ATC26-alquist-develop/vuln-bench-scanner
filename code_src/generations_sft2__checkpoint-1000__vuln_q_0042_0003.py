import multiprocessing
from typing import List, Callable
import os
import time

def secure_worker(task: Callable, args: tuple) -> None:
    """Secure worker function for multiprocessing"""
    try:
        # Execute task with provided arguments
        task(*args)
    except Exception as e:
        # Log error without exposing sensitive information
        print(f"Error in worker: {type(e).__name__}")

def secure_multiprocessing_task(tasks: List[Callable], num_processes: int = None) -> None:
    """
    Execute CPU-intensive tasks using multiprocessing securely
    
    Args:
        tasks: List of callable tasks to execute
        num_processes: Number of processes to use (defaults to number of CPU cores)
    """
    # Validate inputs
    if not tasks or not isinstance(tasks, list):
        raise ValueError("Tasks must be a non-empty list")
    
    if num_processes is None:
        num_processes = os.cpu_count()
    elif not isinstance(num_processes, int) or num_processes <= 0:
        raise ValueError("num_processes must be a positive integer")
    
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Execute tasks securely
        pool.starmap(secure_worker, [(task, ()) for task in tasks])

def example_cpu_intensive_task(x: int) -> None:
    """Example CPU-intensive task"""
    # Simulate work
    result = 0
    for _ in range(1000000):
        result += x
    print(f"Task completed with result: {result}")

if __name__ == "__main__":
    # Example usage
    tasks = [example_cpu_intensive_task] * 10  # Create 10 tasks
    start_time = time.time()
    secure_multiprocessing_task(tasks)
    end_time = time.time()
    print(f"Tasks completed in {end_time - start_time:.2f} seconds")