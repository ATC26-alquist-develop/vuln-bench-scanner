import multiprocessing


def child_process(queue):

    # Child process does some work and sends data back to the parent

    result = "Data from child process"

    queue.put(result)


if __name__ == '__main__':

    # Create a Queue to share data between processes

    queue = multiprocessing.Queue()


    # Create a child process

    child = multiprocessing.Process(target=child_process, args=(queue,))


    # Start the child process

    child.start()


    # Wait for the child process to finish

    child.join()


    # Get the result from the child process

    result = queue.get()

    print(f"Received from child: {result}")

# ===== cell separator =====

import multiprocessing


def child_process(conn):

    # Child process sends data back to the parent

    conn.send("Data from child process")

    conn.close()


if __name__ == '__main__':

    # Create a Pipe

    parent_conn, child_conn = multiprocessing.Pipe()


    # Create a child process

    child = multiprocessing.Process(target=child_process, args=(child_conn,))


    # Start the child process

    child.start()


    # Wait for the child process to finish

    child.join()


    # Get the result from the child process

    result = parent_conn.recv()

    print(f"Received from child: {result}")