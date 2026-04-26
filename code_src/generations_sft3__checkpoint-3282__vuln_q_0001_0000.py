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
        self.processes = []
        self.stop_event = multiprocessing.Event()

    def _worker(self):
        """Worker process function"""
        while not self.stop_event.is_set():
            try:
                task, args, kwargs = self.task_queue.get(timeout=1)
                if self.stop_event.is_set():
                    return
                result = task(*args, **kwargs)
                self.task_queue.task_done()
            except multiprocessing.queues.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in worker: {str(e)}")

    def add_task(self, task: Callable, *args: Any, **kwargs: Any) -> None:
        """Add task to the queue with validation"""
        if not callable(task):
            raise TypeError("Task must be callable")
        validated_args = tuple(validate_input(task)(*args))
        validated_kwargs = {k: validate_input(v) for k, v in kwargs.items()}
        self.task_queue.put((task, validated_args, validated_kwargs))

    def start(self):
        """Start the task pool"""
        for _ in range(self.max_workers):
            p = multiprocessing.Process(target=self._worker)
            p.daemon = True
            p.start()
            self.processes.append(p)

    def stop(self):
        """Safely stop the task pool"""
        self.stop_event.set()
        for p in self.processes:
            p.join(timeout=5)
        self.task_queue.close()
        self.processes.clear()

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()

def example_task(x: int) -> int:
    """Example task that sleeps for x seconds"""
    time.sleep(x)
    return x * 2

if __name__ == "__main__":
    with SecureTaskPool(max_workers=4) as pool:
        for i in range(5):
            pool.add_task(example_task, i)
        
        # Wait for all tasks to complete
        pool.task_queue.join()