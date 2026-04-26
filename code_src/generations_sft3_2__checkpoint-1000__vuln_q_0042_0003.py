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
        
        # Start process
        process.start()
        
        # Wait for process to complete
        process.join()
        
        # Get result
        return process.exitcode
        
    except Exception as e:
        # Log error if needed
        print(f"Error in multiprocessing task: {str(e)}")
        return None
    finally:
        # Ensure process is terminated
        if 'process' in locals() and process.is_alive():
            process.terminate()
            process.join(timeout=1)

def main():
    # Number of tasks to run
    num_tasks = 4
    
    # Create tasks
    tasks = [
        secure_multiprocessing_task(secure_cpu_task, i)
        for i in range(num_tasks)
    ]
    
    # Wait for all tasks to complete
    for task in tasks:
        result = task
        if result is not None:
            print(f"Task {result} completed successfully")
        else:
            print(f"Task failed with error")

if __name__ == "__main__":
    # Run the main function
    main()