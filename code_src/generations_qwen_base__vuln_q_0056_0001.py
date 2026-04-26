import concurrent.futures
import csv
import time

def calculate_factorial(n):
    """Calculate the factorial of a given number."""
    start_time = time.time()
    result = 1
    for i in range(1, n + 1):
        result *= i
    end_time = time.time()
    return result, end_time - start_time

def write_results_to_file(results, filename):
    """Write the results to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Number", "Factorial", "Time"])
        for result in results:
            writer.writerow(result)

def main():
    numbers = [5, 10, 15, 20, 25]  # Example numbers to calculate factorials for
    num_threads = 3  # Number of threads to use

    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks to the executor
        future_to_number = {executor.submit(calculate_factorial, n): n for n in numbers}
        
        # Collect the results
        results = []
        for future in concurrent.futures.as_completed(future_to_number):
            number = future_to_number[future]
            try:
                factorial, time_taken = future.result()
                results.append((number, factorial, time_taken))
            except Exception as exc:
                print(f"Task failed for number {number}: {exc}")

    # Write the results to a CSV file
    write_results_to_file(results, 'factorials_results.csv')

if __name__ == "__main__":
    main()