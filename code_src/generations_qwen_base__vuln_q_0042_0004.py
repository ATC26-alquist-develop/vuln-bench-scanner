import multiprocessing
import time
import random

class Worker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        print(f"Worker {self.name} started")
        while True:
            func, args, kwargs = self.task_queue.get()
            if func is None:
                print(f"Worker {self.name} is terminating")
                break
            try:
                result = func(*args, **kwargs)
                self.result_queue.put(result)
            except Exception as e:
                self.result_queue.put(f"Error: {e}")
        print(f"Worker {self.name} terminated")

def worker_task(task_queue, result_queue):
    while True:
        func, args, kwargs = task_queue.get()
        if func is None:
            break
        try:
            result = func(*args, **kwargs)
            result_queue.put(result)
        except Exception as e:
            result_queue.put(f"Error: {e}")

def main():
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    # Start the worker processes
    num_workers = 4  # Number of worker processes
    workers = [Worker(task_queue, result_queue) for _ in range(num_workers)]
    for worker in workers:
        worker.start()

    # Add tasks to the task queue
    tasks = [
        (random.randint(0, 100), "arg1", {"key": "value"}),
        (random.randint(0, 100), "arg2", {"key": "value"}),
        (random.randint(0, 100), "arg3", {"key": "value"}),
        (random.randint(0, 100), "arg4", {"key": "value"}),
        (random.randint(0, 100), "arg5", {"key": "value"}),
        (random.randint(0, 100), "arg6", {"key": "value"}),
        (random.randint(0, 100), "arg7", {"key": "value"}),
        (random.randint(0, 100), "arg8", {"key": "value"}),
        (random.randint(0, 100), "arg9", {"key": "value"}),
        (random.randint(0, 100), "arg10", {"key": "value"}),
    ]

    for task in tasks:
        task_queue.put(task)

    # Add a None task to signal the worker processes to terminate
    for _ in range(num_workers):
        task_queue.put(None)

    # Collect results
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    # Print results
    for result in results:
        print(result)

    # Wait for worker processes to terminate
    for worker in workers:
        worker.join()

if __name__ == "__main__":
    main()