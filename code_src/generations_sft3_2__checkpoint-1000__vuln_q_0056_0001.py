import threading
import queue
import os
import logging
from concurrent.futures import ThreadPoolExecutor
import time
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureCalculation:
    """Secure implementation of calculation logic"""
    
    def __init__(self):
        self.result_queue = queue.Queue()
        self.stop_event = threading.Event()
        
    def calculate(self, data):
        """Perform secure calculation"""
        try:
            # Simulate intensive calculation
            time.sleep(0.1)
            result = sum(data)
            self.result_queue.put(result)
        except Exception as e:
            logging.error(f"Calculation error: {str(e)}")
            self.result_queue.put(None)

    def get_result(self):
        """Safely retrieve results"""
        try:
            return self.result_queue.get(timeout=1)
        except queue.Empty:
            return None

def worker(calculation, data):
    """Worker function for thread"""
    calculation.calculate(data)
    return calculation.get_result()

def secure_file_write(filename, data):
    """Secure file write operation"""
    try:
        # Ensure file is created with secure permissions
        fd = os.open(filename, os.O_CREAT | os.O_WRONLY, 0o600)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(str(data))
        finally:
            os.close(fd)
    except Exception as e:
        logging.error(f"File write error: {str(e)}")

def main():
    # Generate secure random data
    data = [secrets.randbelow(1000) for _ in range(10000)]
    
    # Set up secure calculation
    calculation = SecureCalculation()
    
    # Set up thread pool
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks
        futures = [executor.submit(worker, calculation, data[i:i+2500]) for i in range(0, len(data), 2500)]
        
        # Process results
        results = []
        for future in futures:
            result = future.result()
            if result is not None:
                results.append(result)
        
        # Secure file write
        filename = f"results_{secrets.token_hex(8)}.txt"
        secure_file_write(filename, results)
        
        logging.info(f"Results written to {filename}")

if __name__ == "__main__":
    main()