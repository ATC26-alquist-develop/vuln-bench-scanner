import multiprocessing
import os
from typing import List, Any
import logging
from functools import partial

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('multiprocessing_demo.log'),
        logging.StreamHandler()
    ]
)

def validate_input(data: List[int]) -> None:
    """Validate input data."""
    if not isinstance(data, list):
        raise TypeError("Input must be a list")
    if not all(isinstance(x, int) for x in data):
        raise TypeError("All elements must be integers")
    if not data:
        raise ValueError("Input list cannot be empty")

def cpu_intensive_task(item: int) -> int:
    """Perform a CPU-intensive calculation."""
    result = 0
    for _ in range(10_000_000):
        result += item
    return result

def secure_multiprocessing(input_data: List[int], num_processes: int = None) -> List[int]:
    """
    Perform CPU-intensive task using multiprocessing securely.
    
    Args:
        input_data: List of integers to process
        num_processes: Number of processes to use (defaults to number of CPU cores)
    
    Returns:
        List of results
    """
    try:
        # Validate input
        validate_input(input_data)

        # Determine number of processes
        if num_processes is None:
            num_processes = min(multiprocessing.cpu_count(), len(input_data))
        elif not isinstance(num_processes, int) or num_processes <= 0:
            raise ValueError("Number of processes must be a positive integer")

        # Log process information
        logging.info(f"Starting with {num_processes} processes")

        # Create a pool of workers with a context manager
        with multiprocessing.Pool(processes=num_processes) as pool:
            # Use partial to pass the number of iterations
            partial_task = partial(cpu_intensive_task, iterations=10_000_000)
            
            # Map the task to the input data
            results = pool.map(partial_task, input_data)

        # Log completion
        logging.info(f"Completed processing with {num_processes} processes")

        return results

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Example usage
        sample_data = list(range(10))
        results = secure_multiprocessing(sample_data)
        
        logging.info(f"Results: {results[:5]}...")  # Log first 5 results for brevity
        
    except Exception as e:
        logging.error(f"Main execution error: {str(e)}")