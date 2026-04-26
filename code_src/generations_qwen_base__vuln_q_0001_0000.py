import multiprocessing
import time

def worker(task_id):
    """Function to be executed in a separate process."""
    print(f"Worker {task_id} started at {time.ctime()}")
    time.sleep(2)  # Simulate some work
    print(f"Worker {task_id} finished at {time.ctime()}")

def main():
    # Number of tasks to be processed
    num_tasks = 5
    
    # Create a list to hold the processes
    processes = []
    
    # Create and start processes
    for i in range(num_tasks):
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)
        p.start()
    
    # Wait for all processes to complete
    for p in processes:
        p.join()
    
    print("All tasks completed.")

if __name__ == "__main__":
    main()