import multiprocessing

def compute(data):
    # Perform some computation on the data
    result = sum(data)
    return result

if __name__ == '__main__':
    # Create a list of large datasets
    datasets = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]

    # Create a pool of worker processes
    pool = multiprocessing.Pool()

    # Map the compute function to each dataset
    results = pool.map(compute, datasets)

    # Close the pool of worker processes
    pool.close()

    # Print the results
    print(results)