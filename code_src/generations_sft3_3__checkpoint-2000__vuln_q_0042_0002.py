import multiprocessing as mp
from multiprocessing import Manager
import os

def child_process(shared_dict):
    # Child process code
    pid = os.getpid()
    shared_dict[str(pid)] = f"Data from child process {pid}"
    return

def main():
    # Create a manager to handle shared objects
    with Manager() as manager:
        # Create a dictionary that can be shared between processes
        shared_dict = manager.dict()
        
        # Create and start child process
        p = mp.Process(target=child_process, args=(shared_dict,))
        p.start()
        p.join()
        
        # Print shared data
        print("Shared data from child process:", dict(shared_dict))
        
    return

if __name__ == '__main__':
    main()