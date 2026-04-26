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
        # Simulate calculation with a delay
        time.sleep(0.1)
        
        # Generate a secure random number for demonstration
        result = secrets.randbelow(1000)
        
        # Thread-safe result storage
        with self.lock:
            self.result_queue.put(result)
        
    def get_result(self):
        """Thread-safe result retrieval"""
        return self.result_queue.get()

def secure_file_write(filename, data):
    """Secure file write operation"""
    try:
        # Ensure the output directory exists and is secure
        output_dir = Path("secure_output")
        output_dir.mkdir(exist_ok=True, mode=0o700)
        
        # Use atomic write operation
        temp_file = output_dir / f"{filename}.{secrets.token_hex(8)}.tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(str(data))
        
        # Atomic rename for data integrity
        temp_file.rename(output_dir / filename)
        
    except Exception as e:
        logging.error(f"Error writing to file: {e}")
        raise

def main():
    # Create calculation worker
    calc = SecureCalculation(max_workers=4)
    
    # Create thread pool
    with ThreadPoolExecutor(max_workers=calc.max_workers) as executor:
        # Simulate data processing
        data_list = [i for i in range(100)]
        
        # Submit tasks
        futures = [executor.submit(calc.calculate, d) for d in data_list]
        
        # Process results
        results = []
        for _ in futures:
            result = calc.get_result()
            results.append(result)
            
            # Secure file write
            secure_file_write(f"result_{result}.txt", result)
            
    logging.info(f"All calculations completed. Results: {results}")

if __name__ == "__main__":
    main()