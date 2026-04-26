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

def secure_multiprocessing(tasks: list[tuple[Callable[[], Any], int]]) -> None:
    """Secure multiprocessing implementation"""
    # Set up signal handler for graceful shutdown
    def signal_handler(signum, frame):
        logger.warning("Shutdown initiated")
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Validate input
    if not isinstance(tasks, list):
        raise ValueError("Tasks must be provided as a list")

    # Create multiprocessing pool with reasonable limits
    max_processes = min(multiprocessing.cpu_count() * 2, 40)  # Limit to 40 max processes
    with multiprocessing.Pool(processes=max_processes) as pool:
        try:
            # Start tasks
            pool.starmap(secure_task, tasks)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        except Exception as e:
            logger.error(f"Error in multiprocessing: {str(e)}")
        finally:
            pool.close()
            pool.join()

if __name__ == "__main__":
    # Example usage
    def example_task(task_id: int) -> None:
        """Example task function"""
        time.sleep(2)
        print(f"Task {task_id} completed")

    tasks = [(example_task, i) for i in range(5)]
    secure_multiprocessing(tasks)