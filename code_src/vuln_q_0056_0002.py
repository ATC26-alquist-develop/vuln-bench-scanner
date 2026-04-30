import multiprocessing
import queue
import time
import secrets

def secure_producer(queue, max_size=100):
    """Secure producer function that generates data and puts it into a queue."""
    while True:
        # Generate secure random data
        data = secrets.token_hex(16)  # 16 bytes of random data
        try:
            queue.put(data, block=True, timeout=1)  # Wait for consumer to process
        except queue.Full:
            print("Queue is full, producer waiting...")
        time.sleep(0.1)  # Small delay to prevent CPU overload

def secure_consumer(queue, max_size=100):
    """Secure consumer function that processes data from the queue."""
    while True:
        try:
            data = queue.get(block=True, timeout=1)  # Wait for producer to add data
            # Process data securely (in this case, just print it)
            print(f"Processed: {data}")
        except queue.Empty:
            print("Queue is empty, consumer waiting...")
        time.sleep(0.1)  # Small delay to prevent CPU overload

if __name__ == '__main__':
    # Create a secure queue with a maximum size
    q = multiprocessing.Queue(maxsize=max_size)
    
    # Create producer and consumer processes
    producer = multiprocessing.Process(target=secure_producer, args=(q,))
    consumer = multiprocessing.Process(target=secure_consumer, args=(q,))
    
    # Start processes
    producer.start()
    consumer.start()
    
    # Join processes (in a real application, you might want to implement a proper shutdown mechanism)
    producer.join()
    consumer.join()