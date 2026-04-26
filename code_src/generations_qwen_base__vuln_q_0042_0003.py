import multiprocessing
import time

# Define a function to be parallelized
def calculate_sum(numbers):
    """Calculate the sum of the list of numbers."""
    return sum(numbers)

# Function to simulate a CPU-intensive task
def cpu_intensive_task(numbers):
    """Simulate a CPU-intensive task by summing the numbers."""
    start_time = time.time()
    result = calculate_sum(numbers)
    end_time = time.time()
    print(f"Task completed in {end_time - start_time:.2f} seconds")
    return result

# List of numbers to be processed
numbers = list(range(1000000))

# Number of processes to use
num_processes = multiprocessing.cpu_count()

# Create a pool of worker processes
with multiprocessing.Pool(processes=num_processes) as pool:
    # Distribute the task to the processes
    result = pool.map(cpu_intensive_task, [numbers] * num_processes)

# Sum the results from all processes
total_sum = sum(result)

# Print the total sum
print(f"Total sum: {total_sum}")