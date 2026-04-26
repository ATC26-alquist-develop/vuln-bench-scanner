import multiprocessing
from multiprocessing import Manager

def worker(shared_data):
    # Child process code
    # Access shared data
    print(f"Child process: {shared_data.value}")
    shared_data.value += 1

def main():
    # Create a manager to handle shared data
    with Manager() as manager:
        # Create a shared value
        shared_data = manager.Value('i', 0)
        
        # Create processes
        processes = []
        for _ in range(3):
            p = multiprocessing.Process(target=worker, args=(shared_data,))
            processes.append(p)
            p.start()
        
        # Wait for all processes to complete
        for p in processes:
            p.join()
            
    # Print final value
    print(f"Final shared value: {shared_data.value}")

if __name__ == '__main__':
    main()