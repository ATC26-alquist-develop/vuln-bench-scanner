import multiprocessing as mp
from multiprocessing import Manager
import os

def child_process(shared_dict):
    # Child process code
    pid = os.getpid()
    shared_dict[str(pid)] = f"Child process {pid} started"
    print(f"Child {pid}: {shared_dict[str(pid)]}")

def main():
    # Create a manager to handle shared objects
    with Manager() as manager:
        # Create a dictionary to share data
        shared_dict = manager.dict()
        
        # Create and start child process
        p = mp.Process(target=child_process, args=(shared_dict,))
        p.start()
        p.join()
        
        # Print shared data
        print(f"Parent: {shared_dict}")
        
        # Wait for child process to finish
        p.join()
        
        # Verify child process data
        if str(os.getpid()) in shared_dict:
            print(f"Child process data: {shared_dict[str(os.getpid())]}")

if __name__ == '__main__':
    main()