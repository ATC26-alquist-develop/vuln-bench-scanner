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
        # Use absolute path to prevent directory traversal
        safe_path = Path(filename).resolve()
        
        # Ensure directory exists
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write with secure permissions
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(data)
        os.chmod(safe_path, 0o600)  # Secure file permissions
        
        return True
    except (IOError, OSError) as e:
        logging.error(f"File write error: {e}")
        return False

def worker(worker_id: int, data_queue: queue.Queue, result_queue: queue.Queue):
    """Worker thread function"""
    while True:
        try:
            data = data_queue.get(timeout=5)
            if data is None:
                break
                
            # Perform calculation
            result = SecureCalculationWorker(result_queue)
            result.calculate(data)
            
            # Securely write result
            result_filename = f"result_{worker_id}.txt"
            result_data = f"Result: {result.result_queue.get()}\n"
            if not secure_file_write(result_filename, result_data):
                logging.warning(f"Failed to write result for worker {worker_id}")
                
        except queue.Empty:
            continue
        except Exception as e:
            logging.error(f"Worker {worker_id} error: {e}")
        finally:
            data_queue.task_done()

def main():
    # Set up secure thread pool
    max_workers = os.cpu_count() or 1
    data_queue = queue.Queue()
    result_queue = queue.Queue()
    
    # Create worker threads
    threads = []
    for i in range(max_workers):
        t = threading.Thread(target=worker, args=(i, data_queue, result_queue))
        t.start()
        threads.append(t)
    
    # Generate sample data
    try:
        data = [secrets.randbelow(1000) for _ in range(1000)]
        for item in data:
            data_queue.put(item)
    except Exception as e:
        logging.error(f"Data generation error: {e}")
        return
    
    # Wait for all tasks to complete
    data_queue.join()
    
    # Signal workers to exit
    for _ in range(max_workers):
        data_queue.put(None)
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    logging.info("Calculation completed")

if __name__ == "__main__":
    main()