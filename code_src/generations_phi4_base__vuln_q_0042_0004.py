import multiprocessing

def long_running_process():
    # Your long-running process code goes here
    # ...

if __name__ == '__main__':
    # Create a new process
    process = multiprocessing.Process(target=long_running_process)

    # Start the process
    process.start()

    # Wait for the process to finish
    process.join()