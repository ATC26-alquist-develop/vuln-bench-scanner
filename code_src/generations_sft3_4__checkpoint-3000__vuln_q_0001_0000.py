import multiprocessing
import time
import logging
from typing import Callable, Any
import signal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_task(task_func: Callable[[], Any], task_id: int) -> None:
    """Secure wrapper for task execution"""
    try:
        logger.info(f"Starting task {task_id}")
        task_func()
        logger.info(f"Completed task {task_id}")
    except Exception as e:
        logger.error(f"Error in task {task_id}: {str(e)}")

def secure_multiprocessing(
    tasks: list[tuple[Callable[[], Any], int]],
    max_workers: int = None
) -> None:
    """
    Secure multiprocessing function with safety controls
    
    Args:
        tasks: List of tuples containing (function, task_id)
        max_workers: Maximum number of worker processes (default: number of CPUs)
    """
    # Validate inputs
    if not isinstance(tasks, list) or not all(isinstance(t, tuple) and len(t) == 2 for t in tasks):
        raise ValueError("Invalid tasks format")
    
    if not isinstance(max_workers, int) or max_workers < 1:
        max_workers = None

    # Set up signal handler
    def signal_handler(signum, frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Configure multiprocessing pool with safety limits
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()

    # Create pool with safety limits
    with multiprocessing.Pool(processes=max_workers, initializer=secure_task) as pool:
        try:
            # Run tasks
            pool.starmap(secure_task, tasks)
        except KeyboardInterrupt:
            logger.info("Interrupt received, shutting down...")
        except Exception as e:
            logger.error(f"Error in multiprocessing: {str(e)}")
        finally:
            pool.close()

if __name__ == "__main__":
    def example_task(task_id: int) -> None:
        """Example task that sleeps"""
        time.sleep(2)
        logger.info(f"Task {task_id} completed")

    # Example usage
    tasks = [(example_task, i) for i in range(5)]
    secure_multiprocessing(tasks)