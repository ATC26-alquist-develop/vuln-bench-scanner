import socket


# Create a socket object

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Define the host and the port

host = 'localhost'

port = 12345


# Bind the socket to the host and port

server_socket.bind((host, port))


# Listen for incoming connections

server_socket.listen(1)

print(f"Server listening on {host}:{port}")


# Accept a connection

client_socket, address = server_socket.accept()

print(f"Connection from {address} has been established.")


# Receive data from the client

data = client_socket.recv(1024).decode('utf-8')

print(f"Received from client: {data}")


# Send a response back to the client

client_socket.sendall(b"Hello from the server!")


# Close the connection

client_socket.close()

server_socket.close()

# ===== cell separator =====

import socket


# Create a socket object

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Define the host and the port

host = 'localhost'

port = 12345


# Connect to the server

client_socket.connect((host, port))


# Send data to the server

client_socket.sendall(b"Hello from the client!")


# Receive a response from the server

data = client_socket.recv(1024).decode('utf-8')

print(f"Received from server: {data}")


# Close the connection

client_socket.close()