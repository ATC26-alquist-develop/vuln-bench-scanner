import multiprocessing
import queue
import time
import logging
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def producer(data_queue: multiprocessing.Queue, num_items: int) -> None:
    """Generate data and put it into the queue."""
    try:
        for i in range(num_items):
            item = f"Data item {i}"
            logging.info(f"Producing: {item}")
            data_queue.put(item, block=False)
            time.sleep(0.1)  # Simulate some work
    except Exception as e:
        logging.error(f"Error in producer: {e}")
    finally:
        logging.info("Producer finished")

def consumer(data_queue: multiprocessing.Queue, num_items: int) -> None:
    """Process data from the queue."""
    try:
        for _ in range(num_items):
            try:
                item = data_queue.get(block=True, timeout=1)
                logging.info(f"Consuming: {item}")
                # Simulate processing
                time.sleep(0.2)
            except queue.Empty:
                continue
    except Exception as e:
        logging.error(f"Error in consumer: {e}")
    finally:
        logging.info("Consumer finished")

def main() -> None:
    # Use a bounded queue to prevent unbounded memory growth
    queue_size = 10
    data_queue: multiprocessing.Queue = multiprocessing.Queue(maxsize=queue_size)

    num_items = 50
    num_processes = 2

    # Create producer and consumer processes
    processes = [
        multiprocessing.Process(target=producer, args=(data_queue, num_items)),
        multiprocessing.Process(target=consumer, args=(data_queue, num_items))
    ]

    try:
        # Start processes
        for p in processes:
            p.start()

        # Wait for processes to complete
        for p in processes:
            p.join()

    except Exception as e:
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()