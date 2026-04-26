import multiprocessing
import time
import random

def producer(queue):
    while True:
        data = random.randint(1, 100)
        print(f'Producer: produced {data}')
        queue.put(data)
        time.sleep(random.random())

def consumer(queue):
    while True:
        data = queue.get()
        print(f'Consumer: consumed {data}')
        time.sleep(random.random())

if __name__ == '__main__':
    queue = multiprocessing.Queue()

    producer_process = multiprocessing.Process(target=producer, args=(queue,))
    consumer_process = multiprocessing.Process(target=consumer, args=(queue,))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()