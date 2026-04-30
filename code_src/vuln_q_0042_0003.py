import multiprocessing
from typing import List, Callable
import os
import time

def secure_worker(task: Callable[[], None], 
                  task_id: int, 
                  result_queue: multiprocessing.Queue) -> None:
    """
    Secure worker function for multiprocessing.
    Runs a given task in a separate process.
    """
    try:
        # Run the task in a separate process
        task()
        # Put the result in the queue
        result_queue.put((task_id, True))
    except Exception as e:
        # Log error without exposing sensitive information
        result_queue.put((task_id, False, str(type(e))))

def secure_multiprocessing(
    tasks: List[Callable[[], None]], 
    num_processes: int = os.cpu_count()
) -> List[bool]:
    """
    Securely execute multiple tasks using multiprocessing.
    Returns a list of boolean results indicating success/failure.
    """
    # Input validation
    if not tasks or not isinstance(tasks, list):
        raise ValueError("Tasks must be a non-empty list")
    if not isinstance(num_processes, int) or num_processes <= 0:
        raise ValueError("Number of processes must be a positive integer")
    if num_processes > os.cpu_count():
        raise ValueError("Number of processes cannot exceed CPU count")

    # Create a queue for results
    result_queue = multiprocessing.Queue()

    # Create and start worker processes
    processes = []
    for i in range(min(num_processes, len(tasks))):
        p = multiprocessing.Process(target=secure_worker, 
                                   args=(tasks[i], i, result_queue))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Collect results
    results = []
    while not result_queue.empty():
        result = result_queue.get()
        if len(result) == 3:
            # Handle error case
            results.append(False)
        else:
            results.append(result[1])

    return results

# Example usage
def example_task():
    # Simulate a CPU-intensive task
    time.sleep(1)
    return True

if __name__ == '__main__':
    tasks = [example_task] * 10  # Create 10 tasks
    results = secure_multiprocessing(tasks)
    print(f"All tasks completed: {all(results)}")