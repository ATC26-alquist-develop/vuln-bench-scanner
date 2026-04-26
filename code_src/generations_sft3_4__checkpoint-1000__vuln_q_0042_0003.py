import multiprocessing
import time
import os
from typing import Callable, Any

def secure_cpu_task(task_id: int, max_iterations: int = 1000000) -> int:
    """
    A CPU-intensive task that performs a simple mathematical operation.
    
    Args:
        task_id: Unique identifier for the task
        max_iterations: Maximum number of iterations to perform
        
    Returns:
        Result of the mathematical operation
    """
    result = 0
    for i in range(max_iterations):
        result += i * task_id
    return result

def secure_multiprocessing_task(func: Callable[[int], Any], 
                               task_id: int, 
                               max_iterations: int = 1000000) -> Any:
    """
    Secure wrapper for multiprocessing that handles process creation and cleanup.
    
    Args:
        func: The function to be executed in a separate process
        task_id: Unique identifier for the task
        max_iterations: Maximum number of iterations to perform
        
    Returns:
        Result of the function execution
    """
    try:
        # Create a secure process with limited resources
        process = multiprocessing.Process(
            target=func,
            args=(task_id, max_iterations),
            name=f"Task-{task_id}"
        )
        
        # Set resource limits
        process.nice(19)  # Lowest priority
        process.start()
        
        # Wait for completion with timeout
        process.join(timeout=30)
        
        if process.is_alive():
            process.terminate()
            process.join()
            raise TimeoutError("Process timed out")
            
        return process.exitcode
        
    except Exception as e:
        # Log error securely (implement secure logging mechanism)
        print(f"Error in task {task_id}: {str(e)}")
        return None

def main():
    # Number of tasks to run
    num_tasks = 4
    
    # Create tasks
    tasks = [secure_multiprocessing_task(secure_cpu_task, i) for i in range(num_tasks)]
    
    # Process results
    results = [task for task in tasks if task is not None]
    
    # Print results
    print(f"Completed tasks: {len(results)}/{num_tasks}")
    print(f"Results: {results}")

if __name__ == "__main__":
    # Validate multiprocessing is available
    if not multiprocessing.get_start_method() == "spawn":
        raise RuntimeError("Multiprocessing not available")
    
    # Run main function
    main()