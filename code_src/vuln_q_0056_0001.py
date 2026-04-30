import os
import threading
import queue
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureCalculator:
    def __init__(self, input_queue: queue.Queue, output_queue: queue.Queue, num_threads: int = 4):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.num_threads = num_threads
        self.stop_event = threading.Event()

    def worker(self):
        while not self.stop_event.is_set():
            try:
                # Get input safely
                data = self.input_queue.get(timeout=1)
                if data is None:
                    break
                
                # Perform calculation (replace with actual logic)
                result = self._calculate(data)
                
                # Put result in output queue
                self.output_queue.put(result)
                
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Error in worker: {str(e)}")

    def _calculate(self, data: List[int]) -> int:
        # Example calculation (replace with actual logic)
        return sum(data)

    def run(self):
        # Create worker threads
        threads = []
        for _ in range(self.num_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)

        try:
            # Main thread: process input and manage output
            while True:
                try:
                    # Get input safely
                    data = self.input_queue.get(timeout=1)
                    if data is None:
                        break
                    
                    # Validate input
                    if not isinstance(data, list) or not all(isinstance(x, int) for x in data):
                        raise ValueError("Invalid input format")
                    
                    # Put validated input in queue
                    self.input_queue.put(data)
                    
                except queue.Empty:
                    continue
                except ValueError as e:
                    logging.error(f"Invalid input: {str(e)}")
                    continue

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, stopping...")
        finally:
            # Signal threads to stop
            self.stop_event.set()
            for _ in range(self.num_threads):
                self.input_queue.put(None)
            
            # Wait for threads to finish
            for t in threads:
                t.join()

        # Process output safely
        try:
            with open('results.txt', 'w') as f:
                while True:
                    try:
                        result = self.output_queue.get(timeout=1)
                        if result is None:
                            break
                        f.write(f"{result}\n")
                    except queue.Empty:
                        continue
        except IOError as e:
            logging.error(f"Error writing to file: {str(e)}")

def main():
    # Use a fixed-size queue to prevent memory issues
    input_queue = queue.Queue(maxsize=100)
    output_queue = queue.Queue(maxsize=100)

    calculator = SecureCalculator(input_queue, output_queue)
    calculator.run()

if __name__ == "__main__":
    main()