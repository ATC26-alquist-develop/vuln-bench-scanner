import threading
import queue
import time
import os
from typing import List, Callable
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureCalculator:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.lock = threading.Lock()
        
    def add_task(self, task: Callable[[], float]) -> None:
        """Add a calculation task to the queue."""
        self.task_queue.put(task)
        
    def process_results(self) -> None:
        """Process results from the result queue."""
        while True:
            try:
                result = self.result_queue.get(timeout=1)
                with self.lock:
                    self._write_result(result)
            except queue.Empty:
                break

    def _write_result(self, result: float) -> None:
        """Securely write result to file."""
        try:
            with open('results.txt', 'a') as f:
                f.write(f"{result}\n")
            logging.info(f"Result written: {result}")
        except IOError as e:
            logging.error(f"Error writing to file: {e}")

    def run(self) -> None:
        """Run the secure multi-threaded calculator."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Start result processing thread
            threading.Thread(target=self.process_results, daemon=True).start()
            
            # Submit tasks to executor
            while not self.task_queue.empty():
                task = self.task_queue.get()
                executor.submit(task)

def intensive_calculation(x: float) -> float:
    """Simulate an intensive calculation."""
    time.sleep(0.1)  # Simulate work
    return x * x

def main():
    calculator = SecureCalculator(max_workers=4)
    
    # Add tasks
    for i in range(10):
        calculator.add_task(lambda x=i: intensive_calculation(x))
    
    # Run calculator
    calculator.run()
    
    logging.info("All calculations completed")

if __name__ == "__main__":
    main()