import multiprocessing

def worker(queue):
    # Example worker function
    data = queue.get()
    print(f"Worker received: {data}")
    # Process data securely here
    return f"Processed: {data}"

def main():
    # Create a Queue for inter-process communication
    queue = multiprocessing.Queue()

    # Start a child process
    child_process = multiprocessing.Process(target=worker, args=(queue,))
    child_process.start()

    # Send data to the child process
    queue.put("Hello, child process!")

    # Wait for the child process to finish
    child_process.join()

    # Retrieve and process the result
    result = queue.get()
    print(f"Parent received: {result}")

if __name__ == "__main__":
    main()