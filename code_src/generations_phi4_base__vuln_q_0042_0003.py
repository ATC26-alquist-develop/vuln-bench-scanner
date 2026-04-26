def calculate_square(n):
    return n * n

# ===== cell separator =====

import multiprocessing

def calculate_squares(numbers):
    with multiprocessing.Pool() as pool:
        squares = pool.map(calculate_square, numbers)
    return squares

# ===== cell separator =====

if __name__ == '__main__':
    numbers = list(range(1, 1000001))  # A list of numbers from 1 to 1,000,000
    squares = calculate_squares(numbers)
    print(squares[:10])  # Print the first 10 squares for demonstration