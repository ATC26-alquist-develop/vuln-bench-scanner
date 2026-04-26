import multiprocessing
import queue
import time
import random
import logging
from typing import List, Callable

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureProducerConsumer:
    def __init__(self, num_consumers: int, data_generator: Callable[[], List[float]]):
        self.num_consumers = num_consumers
        self.data_queue = multiprocessing.Queue(maxsize=100)  # Limit queue size
        self.processed_data = multiprocessing.Value('i', 0)
        
        # Create and start consumers
        self.processors = []
        for _ in range(num_consumers):
            p = multiprocessing.Process(target=self._consumer_worker, args=(self.data_queue, self.processed_data))
            p.start()
            self.processors.append(p)
        
        # Create and start producer
        self.producer = multiprocessing.Process(target=self._producer_worker, args=(data_generator,))
        self.producer.start()

    def _producer_worker(self, data_generator: Callable[[], List[float]]):
        try:
            while True:
                data = data_generator()
                if not self.data_queue.full():
                    self.data_queue.put(data)
                    logging.info(f"Produced data: {len(data)} items")
                else:
                    logging.warning("Queue full, data dropped")
                time.sleep(random.uniform(0.1, 0.5))  # Random delay between 0.1 to 0.5 seconds
        except Exception as e:
            logging.error(f"Producer error: {str(e)}")
        finally:
            self.data_queue.put(None)  # Signal end of data

    def _consumer_worker(self, data_queue: multiprocessing.Queue, processed_data: multiprocessing.Value):
        try:
            while True:
                try:
                    data = data_queue.get(block=True, timeout=1)
                    if data is None:
                        break
                    if data is not None:
                        # Process data (example: sum)
                        result = sum(data)
                        with processed_data.get_lock():
                            processed_data.value += 1
                        logging.info(f"Processed data: {result}")
                except queue.Empty:
                    continue
                except Exception as e:
                    logging.error(f"Consumer error: {str(e)}")
        except Exception as e:
            logging.error(f"Consumer error: {str(e)}")
        finally:
            logging.info("Consumer finished")

    def wait_completion(self):
        self.producer.join()
        for p in self.processors:
            p.join()
        logging.info("All processes completed")

if __name__ == "__main__":
    def generate_data() -> List[float]:
        return [random.uniform(0, 100) for _ in range(10)]

    # Example usage
    try:
        SecureProducerConsumer(num_consumers=3, data_generator=generate_data).wait_completion()
    except Exception as e:
        logging.error(f"Main error: {str(e)}")