import multiprocessing
import time
import logging
from typing import Callable, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def secure_long_running_process(task: Callable[[], Any], 
                               timeout: int = 3600, 
                               interval: int = 60) -> None:
    """
    Run a long-running process in a separate process with security measures.
    
    Args:
        task: The function to execute
        timeout: Maximum execution time in seconds
        interval: Check interval in seconds
    
    Raises:
        multiprocessing.TimeoutError: If process exceeds timeout
        Exception: For any other errors
    """
    try:
        # Create a process with a name and security group
        process = multiprocessing.Process(target=task, name="SecureProcess")
        
        # Set a timeout to prevent indefinite execution
        process.start()
        
        # Monitor process
        start_time = time.time()
        while process.is_alive():
            if time.time() - start_time > timeout:
                process.terminate()
                raise multiprocessing.TimeoutError("Process exceeded timeout")
            
            time.sleep(interval)
        
        # Wait for process to finish
        process.join(timeout=interval)
        
        if process.is_alive():
            process.terminate()
            raise Exception("Process did not finish within expected time")
        
        logging.info("Process completed successfully")
        
    except Exception as e:
        logging.error(f"Process error: {str(e)}")
        raise

def example_task():
    """Example task function"""
    logging.info("Task started")
    time.sleep(5)  # Simulate work
    logging.info("Task completed")

if __name__ == "__main__":
    try:
        secure_long_running_process(example_task)
    except Exception as e:
        logging.error(f"Failed to execute process: {str(e)}")