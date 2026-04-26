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
    def __init__(self):
        self.result_queue = queue.Queue()
        self.stop_event = threading.Event()
        
    def calculate(self, num):
        """Perform secure calculation"""
        try:
            # Simulate intensive calculation
            time.sleep(0.1)
            result = num * 2
            self.result_queue.put(result)
        except Exception as e:
            logging.error(f"Calculation error: {e}")
        finally:
            self.stop_event.set()

class SecureFileWriter:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def write_results(self, results):
        """Securely write results to file"""
        try:
            # Generate unique filename
            filename = f"results_{secrets.token_hex(8)}.txt"
            file_path = self.output_dir / filename
            
            # Write results atomically
            temp_file = file_path.with_suffix('.tmp')
            with temp_file.open('w') as f:
                for result in results:
                    f.write(f"{result}\n")
            
            # Atomic rename
            temp_file.replace(file_path)
            
            logging.info(f"Results written to {file_path}")
        except Exception as e:
            logging.error(f"Writing error: {e}")

def main():
    # Create secure calculation and writer objects
    calc = SecureCalculation()
    writer = SecureFileWriter("secure_output")
    
    # Number of threads
    num_threads = 4
    
    # Generate secure random numbers
    numbers = [secrets.randbelow(1000) for _ in range(100)]
    
    # Process numbers using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for num in numbers:
            futures.append(executor.submit(calc.calculate, num))
        
        # Wait for all calculations to complete
        for future in futures:
            future.result()
        
        # Signal threads to stop
        calc.stop_event.set()
        
        # Collect results
        results = []
        while not calc.result_queue.empty():
            results.append(calc.result_queue.get())
        
        # Write results
        writer.write_results(results)

if __name__ == "__main__":
    main()