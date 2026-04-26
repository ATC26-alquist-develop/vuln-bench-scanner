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
    """Secure calculation class with controlled execution"""
    
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
        
        # Use thread-safe queue to store results
        with self.lock:
            self.result_queue.put((data, result))
        
        return result

def secure_file_write(filename, data):
    """Secure file write operation"""
    try:
        # Ensure output directory exists and is secure
        output_dir = Path("secure_output")
        output_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Use secure file path
        file_path = output_dir / filename
        
        # Write data atomically
        temp_path = file_path.with_suffix('.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(str(data))
        
        # Atomic rename
        os.replace(temp_path, file_path)
        
        # Set secure permissions
        os.chmod(file_path, 0o600)
        
    except Exception as e:
        logging.error(f"Error writing to file: {e}")
        raise

def main():
    # Create secure calculation instance
    calc = SecureCalculation(max_workers=4)
    
    # Create thread pool
    with ThreadPoolExecutor(max_workers=calc.max_workers) as executor:
        # Simulate data processing
        data_list = [i for i in range(100)]
        
        # Submit tasks
        futures = [executor.submit(calc.calculate, d) for d in data_list]
        
        # Process results
        results = []
        for _ in range(len(data_list)):
            results.append(calc.result_queue.get())
        
        # Write results securely
        filename = "secure_results.txt"
        secure_file_write(filename, results)
        
        logging.info(f"Results written to {filename}")

if __name__ == "__main__":
    main()