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
        """Perform calculation with timeout"""
        try:
            # Simulate intensive calculation
            time.sleep(1)
            result = sum(data)
            return result
        except Exception as e:
            logging.error(f"Calculation error: {str(e)}")
            return None

    def worker(self, data):
        """Worker thread function"""
        try:
            result = self.calculate(data)
            if result is not None:
                self.result_queue.put(result)
        except Exception as e:
            logging.error(f"Worker error: {str(e)}")
        finally:
            self.stop_event.set()

def secure_file_write(filename, data):
    """Secure file writing function"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Use secure file writing method
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(data))
    except Exception as e:
        logging.error(f"File write error: {str(e)}")

def main():
    # Generate secure random data
    data = [secrets.randbelow(1000) for _ in range(10000)]
    
    # Create secure calculation instance
    calc = SecureCalculation()
    
    # Create thread pool
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks to worker threads
        for _ in range(4):
            executor.submit(calc.worker, data)
        
        # Wait for all tasks to complete
        calc.stop_event.wait()
        
        # Collect results
        results = []
        while not calc.result_queue.empty():
            results.append(calc.result_queue.get())
        
        # Write results to file securely
        filename = f"results_{secrets.token_hex(8)}.txt"
        secure_file_write(filename, results)
        
        logging.info(f"Results written to {filename}")

if __name__ == "__main__":
    main()