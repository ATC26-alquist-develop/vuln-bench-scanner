import multiprocessing as mp
from multiprocessing import Manager
import os

def child_process(shared_dict):
    # Child process code
    pid = os.getpid()
    shared_dict['child_pid'] = pid
    shared_dict['child_status'] = 'running'
    
    # Example of safe data sharing
    shared_dict['shared_list'].append(pid)

def main():
    # Create a manager to handle shared objects
    with Manager() as manager:
        # Create a shared dictionary
        shared_dict = manager.dict()
        
        # Create and start child process
        child = mp.Process(target=child_process, args=(shared_dict,))
        child.start()
        
        # Wait for child process to finish
        child.join()
        
        # Access shared data
        print(f"Child PID: {shared_dict['child_pid']}")
        print(f"Child status: {shared_dict['child_status']}")
        print(f"Shared list: {list(shared_dict.keys())}")
        
        # Clean up
        child.terminate()
        child.join(timeout=1)
        
if __name__ == '__main__':
    main()