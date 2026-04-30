import multiprocessing
from typing import List, Callable
import os

def secure_worker(task: Callable, data: List[int], result_queue: multiprocessing.Queue) -> None:
    """Secure worker function for multiprocessing."""
    try:
        result = task(data)
        result_queue.put(result)
    except Exception as e:
        result_queue.put(f"Error: {str(e)}")

def secure_cpu_intensive_task(data: List[int]) -> int:
    """Example CPU-intensive task with security measures."""
    if not isinstance(data, list) or not all(isinstance(x, int) for x in data):
        raise ValueError("Input must be a list of integers")
    if len(data) > 1000000:  # Limit input size
        raise ValueError("Input list too large")
    return sum(x * x for x in data)

def secure_multiprocessing_task(data: List[int]) -> int:
    """Securely execute CPU-intensive task using multiprocessing."""
    if not data:
        return 0
    
    num_processes = min(multiprocessing.cpu_count(), len(data) // 1000000 + 1)
    chunk_size = len(data) // num_processes
    result_queue = multiprocessing.Queue()
    
    processes = []
    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(data)
        chunk = data[start:end]
        p = multiprocessing.Process(target=secure_worker, args=(secure_cpu_intensive_task, chunk, result_queue))
        processes.append(p)
        p.start()
    
    total_result = 0
    for _ in range(num_processes):
        result = result_queue.get()
        if isinstance(result, str) and result.startswith("Error:"):
            raise RuntimeError(result)
        total_result += result
    
    for p in processes:
        p.join(timeout=10)  # Prevent hanging
        if p.is_alive():
            p.terminate()
            raise RuntimeError("Process timed out")
    
    return total_result