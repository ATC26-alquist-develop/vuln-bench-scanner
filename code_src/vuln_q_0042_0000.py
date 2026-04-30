import multiprocessing as mp
from typing import List, Union
import os
import logging
from functools import partial

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='parallel_computation.log'
)

def validate_input(data: Union[List, np.ndarray]) -> None:
    """Validate input data for security and type safety."""
    if not data:
        raise ValueError("Input data cannot be empty")
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError("Input must be a list or numpy array")
    if not all(isinstance(x, (int, float, np.number)) for x in data):
        raise TypeError("Input must contain only numeric values")

def secure_chunked_processing(chunk: List[Union[int, float]]) -> List[Union[int, float]]:
    """Process a chunk of data securely."""
    # Example processing: square each element
    return [x ** 2 for x in chunk]

def parallel_computation(data: Union[List, np.ndarray], 
                         num_processes: int = None) -> List[Union[int, float]]:
    """
    Perform parallel computation on data using multiprocessing.
    
    Args:
        data: Input data to process
        num_processes: Number of processes to use (defaults to CPU count)
        
    Returns:
        Processed data
        
    Raises:
        ValueError: If input validation fails
        RuntimeError: If computation fails
    """
    try:
        # Validate input
        validate_input(data)
        
        # Validate number of processes
        if num_processes is None:
            num_processes = os.cpu_count()
        elif not isinstance(num_processes, int) or num_processes <= 0:
            raise ValueError("Number of processes must be a positive integer")
        
        # Log the start of computation
        logging.info(f"Starting parallel computation with {num_processes} processes")
        
        # Create a pool of worker processes
        with mp.Pool(processes=num_processes) as pool:
            # Split data into chunks
            chunk_size = len(data) // num_processes
            chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
            
            # Process chunks in parallel
            try:
                results = pool.map(
                    partial(secure_chunked_processing),
                    chunks
                )
            except Exception as e:
                logging.error(f"Error during parallel computation: {str(e)}")
                raise RuntimeError(f"Computation failed: {str(e)}")
            
            # Combine results
            final_result = [item for sublist in results for item in sublist]
            
            # Log completion
            logging.info(f"Completed parallel computation")
            
            return final_result
    
    except Exception as e:
        logging.error(f"Error in parallel_computation: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        # Generate sample data
        sample_data = list(range(1000000))
        
        # Perform computation
        result = parallel_computation(sample_data)
        
        # Log success
        logging.info(f"Successfully processed {len(result)} items")
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        raise