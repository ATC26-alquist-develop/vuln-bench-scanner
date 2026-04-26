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
        self.output_file = None
        
    def setup_file(self):
        """Securely create output file"""
        try:
            # Create output directory if it doesn't exist
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate secure filename
            filename = f"results_{secrets.token_hex(8)}.txt"
            self.output_file = self.output_dir / filename
            
            # Ensure file permissions are secure
            self.output_file.touch(mode=0o600, exist_ok=True)
        except Exception as e:
            logging.error(f"File setup error: {e}")
            raise
            
    def write_results(self, results):
        """Securely write results to file"""
        try:
            if not self.output_file:
                raise ValueError("Output file not initialized")
                
            with self.output_file.open('a') as f:
                for result in results:
                    f.write(f"{result}\n")
        except Exception as e:
            logging.error(f"Writing to file error: {e}")
            raise

def main():
    try:
        # Initialize secure calculation and writer
        calc = SecureCalculation()
        writer = SecureFileWriter("secure_output")
        
        # Set up output file
        writer.setup_file()
        
        # Create thread pool
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit calculation tasks
            for i in range(100):
                executor.submit(calc.calculate, i)
            
            # Wait for calculations to complete
            calc.stop_event.wait()
            
            # Write results
            results = []
            while not calc.result_queue.empty():
                results.append(calc.result_queue.get())
                
            writer.write_results(results)
            
        logging.info("Calculation completed successfully")
        
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main()