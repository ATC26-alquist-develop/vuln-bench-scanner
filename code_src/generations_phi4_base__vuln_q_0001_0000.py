import multiprocessing

def worker(num):
    print(f'Worker {num} is starting')
    print(f'Worker {num} is done')

if __name__ == '__main__':
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()