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
    
    # Safe way to exit
    mp.current_process().exitcode = 0

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
        
        # Check child status
        if shared_dict['child_status'] == 'running':
            print(f"Child process {shared_dict['child_pid']} completed")
        else:
            print(f"Child process failed with status: {shared_dict['child_status']}")
            
        # Access shared data
        print(f"Shared list from child: {shared_dict['shared_list']}")
        
        # Clean up
        child.terminate()
        child.join(timeout=1)

if __name__ == '__main__':
    main()