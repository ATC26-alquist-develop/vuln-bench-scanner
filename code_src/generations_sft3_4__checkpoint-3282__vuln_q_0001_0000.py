import multiprocessing
import os
from typing import Callable, List, Any
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_input(func: Callable) -> Callable:
    """Decorator to validate input parameters"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Validate input parameters
        if not all(isinstance(arg, (int, float, str, bool)) for arg in args):
            raise ValueError("Invalid input types")
        if not all(isinstance(k, str) and isinstance(v, (int, float, str, bool)) 
                  for k, v in kwargs.items()):
            raise ValueError("Invalid keyword arguments")
        return func(*args, **kwargs)
    return wrapper

class SecureTaskPool:
    def __init__(self, max_workers: int = None):
        """Initialize task pool with safety limits"""
        if max_workers is None:
            max_workers = min(32, os.cpu_count() or 1)
        self.max_workers = max(1, min(32, max(1, max_workers)))
        self.task_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()
        self.process_pool = []
        
    def _worker(self):
        """Worker process function"""
        while True:
            try:
                task, args, kwargs = self.task_queue.get()
                if task is None:
                    break
                result = task(*args, **kwargs)
                self.result_queue.put(result)
            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
                break

    def start(self):
        """Start worker processes"""
        for _ in range(self.max_workers):
            p = multiprocessing.Process(target=self._worker)
            p.daemon = True
            p.start()
            self.process_pool.append(p)

    def stop(self):
        """Stop worker processes"""
        for _ in range(self.max_workers):
            self.task_queue.put((None, None, None))
        for p in self.process_pool:
            p.join(timeout=5)
            if p.is_alive():
                p.terminate()

    @validate_input
    def submit(self, task: Callable, *args, **kwargs) -> Any:
        """Submit a task for execution"""
        if not callable(task):
            raise ValueError("Task must be callable")
        self.task_queue.put((task, args, kwargs))
        return self.result_queue.get()

def secure_multiprocessing(tasks: List[Callable], args_list: List[Any], 
                          kwargs_list: List[dict]) -> List[Any]:
    """
    Securely execute multiple tasks in parallel
    
    Args:
        tasks: List of callable tasks to execute
        args_list: List of tuples containing arguments for each task
        kwargs_list: List of dictionaries containing keyword arguments for each task
    
    Returns:
        List of results from executed tasks
    """
    pool = SecureTaskPool()
    try:
        pool.start()
        results = []
        for task, args, kwargs in zip(tasks, args_list, kwargs_list):
            result = pool.submit(task, *args, **kwargs)
            results.append(result)
        return results
    finally:
        pool.stop()

# Example usage
def example_task(x: int) -> int:
    """Example task that squares its input"""
    return x * x

if __name__ == "__main__":
    # Example of running multiple tasks
    tasks = [example_task] * 5
    args = [(i,) for i in range(10)]
    kwargs = [{}, {}, {}, {}, {}]
    
    results = secure_multiprocessing(tasks, args, kwargs)
    logger.info(f"Results: {results}")