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
        # Create a new process with limited resources
        process = multiprocessing.Process(
            target=func,
            args=(task_id, max_iterations),
            name=f"Task-{task_id}"
        )
        
        # Set process priority to normal
        process.nice(0)
        
        # Start the process
        process.start()
        
        # Wait for completion with timeout
        process.join(timeout=30)
        
        # Check process status
        if process.is_alive():
            process.terminate()
            process.join()
            raise TimeoutError("Process timed out")
            
        return process.exitcode
        
    except Exception as e:
        # Log error here if needed
        return None

def main():
    # Number of tasks to run
    num_tasks = 4
    
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=num_tasks) as pool:
        # Run tasks in parallel
        results = pool.starmap(
            secure_multiprocessing_task,
            [(i, 1000000) for i in range(num_tasks)]
        )
        
    # Print results
    for i, result in enumerate(results):
        print(f"Task {i}: Result = {result}")

if __name__ == "__main__":
    # Validate multiprocessing is available
    if not multiprocessing.get_start_method() == "spawn":
        raise RuntimeError("Multiprocessing not available")
    
    # Run the main function
    main()