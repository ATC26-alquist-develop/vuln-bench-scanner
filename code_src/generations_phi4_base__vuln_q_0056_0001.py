import threading
import time

# Function to perform intensive calculations
def intensive_calculation(start, end, results, thread_id):
    for i in range(start, end):
        result = i * i  # Intensive calculation (square of the number)
        results.append((thread_id, i, result))
        time.sleep(0.01)  # Simulate intensive calculation time

# Function to write results to a file
def write_results_to_file(results, filename):
    with open(filename, 'w') as f:
        for thread_id, number, result in results:
            f.write(f'Thread {thread_id}: {number}^2 = {result}\n')

# Main function to set up threads and start the calculation
def main():
    num_threads = 4
    num_numbers = 100
    results = []
    threads = []
    filename = 'results.txt'

    # Calculate the range of numbers for each thread
    range_per_thread = num_numbers // num_threads

    # Create and start threads
    for i in range(num_threads):
        start = i * range_per_thread
        end = (i + 1) * range_per_thread
        thread = threading.Thread(target=intensive_calculation, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Write results to file
    write_results_to_file(results, filename)
    print(f'Results written to {filename}')

if __name__ == '__main__':
    main()