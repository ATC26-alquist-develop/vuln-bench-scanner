import os
import threading
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List
import hashlib
import secrets

# Set up secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='secure_app.log',
    filemode='a'
)
logger = logging.getLogger()

# Secure file path
RESULTS_FILE = os.path.abspath('secure_results.txt')

# Thread-safe counter for results
results_lock = threading.Lock()
results_count = 0

def secure_hash(data: str) -> str:
    """Create a secure hash of the data."""
    return hashlib.sha256(data.encode()).hexdigest()

def validate_input(data: str) -> bool:
    """Validate input data to prevent injection attacks."""
    # Implement strict input validation
    return data.isalnum() and len(data) <= 100

def perform_intensive_calculation(data: str) -> str:
    """Perform a CPU-intensive calculation."""
    # Simulate calculation with a dummy operation
    result = ''.join(chr((ord(c) * 3) % 256) for c in data)
    return result

def write_result(result: str) -> None:
    """Thread-safe function to write results to file."""
    global results_count
    with results_lock:
        results_count += 1
        # Use a thread-safe way to append to file
        with open(RESULTS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"Result {results_count}: {result}\n")

def worker(data: str) -> None:
    """Worker function for thread pool."""
    try:
        if not validate_input(data):
            logger.warning(f"Invalid input: {data}")
            return

        result = perform_intensive_calculation(data)
        write_result(result)
        logger.info(f"Processed: {data}")
    except Exception as e:
        logger.error(f"Error processing {data}: {str(e)}")

def main():
    # Generate a secure random token for the session
    session_token = secrets.token_hex(16)
    logger.info(f"Session started with token: {session_token}")

    try:
        # Get input data securely (replace with actual secure input method)
        input_data = input("Enter data (max 100 alphanumeric characters): ").strip()

        # Validate input
        if not input_data:
            raise ValueError("No input provided")

        # Limit number of threads to prevent resource exhaustion
        max_threads = min(os.cpu_count() or 1, 4)
        
        # Use ThreadPoolExecutor for managed concurrency
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            # Submit tasks with input validation
            for _ in range(10):  # Process 10 items as an example
                executor.submit(worker, input_data)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        # Clean up: remove the session token from memory
        session_token = None
        logger.info("Session ended")

if __name__ == "__main__":
    main()