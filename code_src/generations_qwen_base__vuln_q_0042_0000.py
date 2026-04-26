import multiprocessing

def square_number(number):
    """Square the given number."""
    return number * number

# ===== cell separator =====

import multiprocessing
import random
import time

def main():
    # Generate a large dataset
    dataset_size = 1000000
    dataset = [random.randint(1, 1000000) for _ in range(dataset_size)]

    # Start time before parallel processing
    start_time = time.time()

    # Create a pool of worker processes
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        # Apply the function to the dataset in parallel
        results = pool.map(square_number, dataset)

    # End time after parallel processing
    end_time = time.time()

    # Print the time taken
    print(f"Time taken to process {dataset_size} numbers in parallel: {end_time - start_time} seconds")

    # Optionally, print the first few results to verify correctness
    print("First 10 results:", results[:10])

if __name__ == "__main__":
    main()