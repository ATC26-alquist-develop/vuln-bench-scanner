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

class SecureCalculation:
    """Secure calculation class with thread-safe operations"""
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.result_queue = queue.Queue()
        self.lock = threading.Lock()
        
    def calculate(self, data):
        """Perform secure calculation"""
        # Simulate calculation with a secure random number
        result = secrets.randbelow(1000) + data
        with self.lock:
            self.result_queue.put(result)
        return result

def worker(calc, data_queue, result_file):
    """Worker thread to process data"""
    while True:
        try:
            data = data_queue.get(timeout=5)  # 5 second timeout
            if data is None:
                break
            result = calc.calculate(data)
            write_result(result, result_file)
            data_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            logging.error(f"Error in worker: {e}")

def write_result(result, result_file):
    """Securely write result to file"""
    try:
        # Ensure directory exists
        Path(result_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Write with atomic operation
        temp_file = f"{result_file}.tmp"
        with open(temp_file, 'w') as f:
            f.write(f"{result}\n")
        os.replace(temp_file, result_file)
    except Exception as e:
        logging.error(f"Error writing result: {e}")

def main():
    # Generate secure random number for seed
    seed = secrets.randbelow(1000000)
    logging.info(f"Using seed: {seed}")
    
    # Initialize calculation class with secure random seed
    calc = SecureCalculation(max_workers=4)
    
    # Generate data
    data = [i for i in range(1000)]
    
    # Create data queue
    data_queue = queue.Queue()
    for d in data:
        data_queue.put(d)
    
    # Create result file
    result_file = "results.txt"
    
    # Create and start worker threads
    threads = []
    for _ in range(calc.max_workers):
        t = threading.Thread(target=worker, args=(calc, data_queue, result_file))
        t.start()
        threads.append(t)
    
    # Wait for all data to be processed
    data_queue.join()
    
    # Signal threads to exit
    for _ in range(calc.max_workers):
        data_queue.put(None)
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    logging.info("Calculation completed")

if __name__ == "__main__":
    main()