import multiprocessing
import signal
import time
from typing import Callable, Any

class SecureProcess(multiprocessing.Process):
    def __init__(self, target: Callable[..., Any], args: tuple = (), kwargs: dict = None):
        super().__init__()
        self._target = target
        self._args = args
        self._kwargs = kwargs or {}
        self._stop_event = multiprocessing.Event()

    def run(self):
        try:
            self._target(*self._args, **self._kwargs)
        except Exception as e:
            print(f"Error in process: {e}")
        finally:
            self._stop_event.set()

    def stop(self):
        self._stop_event.set()

def safe_long_running_process(target: Callable[..., Any], args: tuple = (), kwargs: dict = None) -> SecureProcess:
    """
    Creates a secure long-running process with proper error handling and graceful termination.
    """
    process = SecureProcess(target, args, kwargs)
    process.start()
    return process

def signal_handler(signum, frame):
    """
    Signal handler for graceful termination of processes.
    """
    print("Received termination signal. Shutting down...")
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    def long_running_task():
        try:
            while True:
                print("Working...")
                time.sleep(1)
        except KeyboardInterrupt:
            print("Process interrupted. Shutting down...")
        finally:
            print("Process shutting down.")

    process = safe_long_running_process(long_running_task)
    try:
        process.join()
    except KeyboardInterrupt:
        print("Main process interrupted. Shutting down...")
        process.stop()
        process.join()