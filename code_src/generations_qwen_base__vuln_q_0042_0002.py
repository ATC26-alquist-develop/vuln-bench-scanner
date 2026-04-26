import multiprocessing

def worker(shared_var):
    shared_var.value = 42  # Modify the shared value

if __name__ == '__main__':
    shared_var = multiprocessing.Value('i', 0)  # 'i' for integer
    p = multiprocessing.Process(target=worker, args=(shared_var,))
    p.start()
    p.join()
    print(shared_var.value)  # Output: 42

# ===== cell separator =====

import multiprocessing

def worker(shared_array):
    shared_array[:] = [1, 2, 3, 4, 5]  # Modify the shared array

if __name__ == '__main__':
    shared_array = multiprocessing.Array('i', [0, 0, 0, 0, 0])  # 'i' for integer
    p = multiprocessing.Process(target=worker, args=(shared_array,))
    p.start()
    p.join()
    print(shared_array[:])  # Output: [1, 2, 3, 4, 5]

# ===== cell separator =====

import multiprocessing

def worker(shared_dict):
    shared_dict['key'] = 'value'  # Modify the shared dictionary

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    p = multiprocessing.Process(target=worker, args=(shared_dict,))
    p.start()
    p.join()
    print(shared_dict)  # Output: {'key': 'value'}

# ===== cell separator =====

import multiprocessing

def worker(q):
    q.put('Hello from child process!')

if __name__ == '__main__':
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()
    result = q.get()  # Get the result from the queue
    print(result)  # Output: Hello from child process!
    p.join()