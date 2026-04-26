import threading
import queue
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import time
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureCalculationWorker:
    def __init__(self, result_queue: queue.Queue):
        self.result_queue = result_queue

    def calculate(self, data: int) -> int:
        """Perform secure calculation"""
        # Simulate intensive calculation
        time.sleep(0.1)
        return data * 2

def secure_file_write(filename: str, data: str) -> bool:
    """Secure file write operation"""
    try:
        # Ensure directory exists
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        # Use secure file writing
        temp_filename = f"{filename}.{secrets.token_hex(16)}.tmp"
        with open(temp_filename, 'w', encoding='utf-8') as f:
            f.write(data)
        
        # Atomic rename for data integrity
        os.replace(temp_filename, filename)
        return True
    except Exception as e:
        logging.error(f"File write error: {str(e)}")
        return False

def worker(task_queue: queue.Queue, result_queue: queue.Queue):
    """Worker function for thread pool"""
    while True:
        try:
            data = task_queue.get(timeout=5)
            if data is None:
                break
            result = SecureCalculationWorker(result_queue).calculate(data)
            result_queue.put(result)
            task_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            logging.error(f"Worker error: {str(e)}")

def main():
    # Set up secure task queue
    task_queue = queue.Queue()
    result_queue = queue.Queue()

    # Create thread pool
    num_threads = min(os.cpu_count() or 1, 4)  # Limit max threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit worker threads
        workers = [executor.submit(worker, task_queue, result_queue) for _ in range(num_threads)]

        # Generate sample data
        data = [i for i in range(1000)]

        # Add tasks to queue
        for item in data:
            task_queue.put(item)

        # Wait for tasks to complete
        task_queue.join()

        # Signal workers to exit
        for _ in workers:
            task_queue.put(None)

        # Collect results
        results = []
        while not result_queue.empty():
            results.append(result_queue.get())

        # Write results securely
        if results:
            filename = "results.txt"
            data_to_write = "\n".join(map(str, results))
            if secure_file_write(filename, data_to_write):
                logging.info(f"Results written to {filename}")
            else:
                logging.error("Failed to write results to file")
        else:
            logging.warning("No results to write")

if __name__ == "__main__":
    main()