import multiprocessing
import time
import logging
from typing import Callable, Any
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_input(func: Callable) -> Callable:
    """Decorator to validate function inputs"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Validate inputs here
        if not all(isinstance(arg, (int, float, str)) for arg in args):
            raise ValueError("Invalid input types")
        if not all(isinstance(k, str) and isinstance(v, (int, float, str)) 
                  for k, v in kwargs.items()):
            raise ValueError("Invalid keyword arguments")
        return func(*args, **kwargs)
    return wrapper

class SecureTaskPool:
    def __init__(self, max_workers: int = None):
        """Initialize task pool with safety limits"""
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.task_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()
        self.processes: list[multiprocessing.Process] = []
        
    def _worker(self):
        """Worker process with proper error handling"""
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
            p.start()
            self.processes.append(p)

    def stop(self):
        """Safely stop worker processes"""
        for _ in self.processes:
            self.task_queue.put(None)
        for p in self.processes:
            p.join(timeout=5)
        self.processes.clear()

    @validate_input
    def submit(self, task: Callable, *args, **kwargs) -> Any:
        """Submit a task for execution"""
        if not callable(task):
            raise TypeError("Task must be callable")
        self.task_queue.put((task, args, kwargs))
        return self.result_queue.get()

def example_task(x: int) -> int:
    """Example task that sleeps and returns"""
    time.sleep(1)
    return x * 2

def main():
    """Main function demonstrating secure usage"""
    try:
        pool = SecureTaskPool(max_workers=4)
        pool.start()

        # Submit tasks
        results = []
        for i in range(5):
            result = pool.submit(example_task, i)
            results.append(result)

        # Process results
        for result in results:
            logger.info(f"Task result: {result}")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        pool.stop()

if __name__ == "__main__":
    main()