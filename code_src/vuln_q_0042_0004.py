import multiprocessing
import time
import os

def secure_background_process(task_id):
    """
    Securely run a long-running background process.
    
    Args:
        task_id (int): Unique identifier for the task
    """
    # Validate task_id to prevent injection attacks
    if not isinstance(task_id, int) or task_id < 0:
        raise ValueError("Invalid task_id")

    # Set a secure working directory
    working_dir = os.path.join(os.getcwd(), "secure_work_dir")
    os.makedirs(working_dir, exist_ok=True)

    try:
        # Run the long-running task
        while True:
            # Simulate work
            time.sleep(60)  # Sleep for 60 seconds
            print(f"Task {task_id} is running in {working_dir}")
    except KeyboardInterrupt:
        print(f"Task {task_id} stopped")
    except Exception as e:
        print(f"Error in Task {task_id}: {str(e)}")
    finally:
        # Clean up resources
        print(f"Cleaning up resources for Task {task_id}")
        # Remove the working directory
        try:
            os.rmdir(working_dir)
        except OSError:
            pass

def main():
    # Get the number of CPU cores
    num_cores = multiprocessing.cpu_count()

    # Create and start background processes
    processes = []
    for i in range(num_cores):
        p = multiprocessing.Process(target=secure_background_process, args=(i,))
        p.start()
        processes.append(p)

    # Wait for processes to complete (they won't in this case)
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()