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
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.result_queue = queue.Queue()
        self.lock = threading.Lock()
        
        # Ensure output directory exists and has proper permissions
        self.output_dir = Path("secure_output")
        self.output_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    def calculate(self, data):
        """Perform secure calculation"""
        try:
            # Simulate calculation with a sleep
            time.sleep(0.1)
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
                with self.lock:
                    self.result_queue.put(result)
            else:
                logging.warning("Calculation failed")
        except Exception as e:
            logging.error(f"Worker error: {str(e)}")

    def process_data(self, data_list):
        """Process data using thread pool"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for data in data_list:
                executor.submit(self.worker, data)

    def write_results(self):
        """Securely write results to file"""
        try:
            # Generate a random filename
            filename = f"results_{secrets.token_hex(8)}.txt"
            file_path = self.output_dir / filename

            # Write results atomically
            with file_path.open("w") as f:
                while not self.result_queue.empty():
                    result = self.result_queue.get()
                    f.write(f"{result}\n")
                    f.flush()
                    os.fsync(f.fileno())

            logging.info(f"Results written to {file_path}")
        except Exception as e:
            logging.error(f"Writing error: {str(e)}")

def main():
    # Example usage
    calc = SecureCalculation(max_workers=4)
    data_list = [[i] * 1000 for i in range(100)]  # Example data
    
    calc.process_data(data_list)
    calc.write_results()

if __name__ == "__main__":
    main()