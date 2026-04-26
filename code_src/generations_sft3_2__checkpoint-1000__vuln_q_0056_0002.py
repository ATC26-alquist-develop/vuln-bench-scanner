import multiprocessing
import queue
import time
import random

def producer(queue, stop_event):
    """Generate data and put it in the queue."""
    while not stop_event.is_set():
        try:
            # Generate some random data
            data = random.randint(1, 100)
            queue.put(data)
            print(f"Produced: {data}")
            time.sleep(random.uniform(0.1, 0.5))  # Random delay between 0.1 to 0.5 seconds
        except queue.Full:
            print("Queue is full, producer stopped")
            break
        except Exception as e:
            print(f"Error in producer: {e}")
            break

def consumer(queue, stop_event):
    """Process data from the queue."""
    while not stop_event.is_set():
        try:
            data = queue.get(timeout=1)
            print(f"Consumed: {data}")
            # Simulate processing time
            time.sleep(random.uniform(0.1, 0.3))
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error in consumer: {e}")
            break

def main():
    # Create a multiprocessing-safe queue
    queue = multiprocessing.Queue(maxsize=100)
    
    # Create and start producer and consumer processes
    stop_event = multiprocessing.Event()
    producer_process = multiprocessing.Process(target=producer, args=(queue, stop_event))
    consumer_process = multiprocessing.Process(target=consumer, args=(queue, stop_event))
    
    try:
        producer_process.start()
        consumer_process.start()
        
        # Run for 10 seconds
        time.sleep(10)
        
        # Stop processes
        stop_event.set()
        producer_process.join()
        consumer_process.join()
        
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        # Ensure queue is closed
        if not queue.empty():
            queue.close()
        queue.join_thread()

if __name__ == "__main__":
    main()