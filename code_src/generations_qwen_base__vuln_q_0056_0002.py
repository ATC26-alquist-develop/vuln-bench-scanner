import multiprocessing
import random
import time

# Shared queue to communicate between producer and consumer
queue = multiprocessing.Queue(maxsize=10)

def producer(queue):
    while True:
        # Generate some data
        data = random.randint(1, 100)
        print(f"Produced: {data}")
        # Put data into the queue
        queue.put(data)
        time.sleep(1)  # Simulate some delay

def consumer(queue):
    while True:
        # Get data from the queue
        data = queue.get()
        print(f"Consumed: {data}")
        time.sleep(2)  # Simulate some delay

if __name__ == "__main__":
    # Create producer and consumer processes
    producer_process = multiprocessing.Process(target=producer, args=(queue,))
    consumer_process = multiprocessing.Process(target=consumer, args=(queue,))

    # Start processes
    producer_process.start()
    consumer_process.start()

    # Wait for processes to finish
    producer_process.join()
    consumer_process.join()