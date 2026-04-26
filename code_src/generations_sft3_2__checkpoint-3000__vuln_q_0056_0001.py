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

def worker(calc, data_queue, result_queue):
    """Worker thread to process data"""
    while True:
        try:
            data = data_queue.get(timeout=5)  # 5 second timeout
            if data is None:
                break
            result = calc.calculate(data)
            result_queue.put(result)
        except queue.Empty:
            continue
        finally:
            data_queue.task_done()

def secure_file_write(filename, data):
    """Secure file write operation"""
    try:
        # Ensure directory exists
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        # Write with secure permissions
        with open(filename, 'w', encoding='utf-8') as f:
            os.chmod(filename, 0o600)  # Read/write for owner only
            f.write(str(data))
        logging.info(f"Results written to {filename}")
    except IOError as e:
        logging.error(f"Error writing to file: {e}")
        raise

def main():
    # Create calculation object
    calc = SecureCalculation(max_workers=4)
    
    # Create data queue
    data_queue = queue.Queue()
    
    # Create result queue
    result_queue = queue.Queue()
    
    # Create worker threads
    threads = []
    for _ in range(calc.max_workers):
        t = threading.Thread(target=worker, args=(calc, data_queue, result_queue))
        t.start()
        threads.append(t)
    
    try:
        # Add data to queue
        for i in range(100):
            data_queue.put(i)
        
        # Wait for all data to be processed
        data_queue.join()
        
        # Signal workers to exit
        for _ in range(calc.max_workers):
            data_queue.put(None)
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        # Collect results
        results = []
        while not result_queue.empty():
            results.append(result_queue.get())
        
        # Write results securely
        filename = 'results.txt'
        secure_file_write(filename, results)
        
        logging.info("Calculation completed successfully")
    
    except Exception as e:
        logging.error(f"Calculation failed: {e}")
        raise

if __name__ == "__main__":
    main()