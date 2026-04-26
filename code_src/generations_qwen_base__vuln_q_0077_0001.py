import pickle
import socket

def server_program():
    # Get the hostname
    host = socket.gethostname()
    port = 5000  # Reserve a port for your service.

    server_socket = socket.socket()  # Get instance
    # Look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = pickle.loads(data)  # deserialize the object
        print("Deserialized object: ", data)
        data = input(' -> ')  # send back the deserialized object
        conn.send(pickle.dumps(data))  # send data to the client

    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()

# ===== cell separator =====

import pickle
import socket

def client_program():
    host = socket.gethostname()  # both ends will be connected to the same host
    port = 5000  # initilize port no. 

    client_socket = socket.socket()  # instantiate
    # connect to the server
    client_socket.connect((host, port))

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(pickle.dumps(message))  # send message
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()