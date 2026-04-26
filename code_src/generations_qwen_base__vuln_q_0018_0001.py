import socket

# Define the server's IP address and port
SERVER_IP = '127.0.0.1'  # The server can be any IP address, but '127.0.0.1' is localhost
SERVER_PORT = 65432     # Choose any unused port number

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server's IP address and port
server_socket.bind((SERVER_IP, SERVER_PORT))

# Listen for incoming connections (max 5 connections in the queue)
server_socket.listen(5)
print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}")

while True:
    # Accept a connection from a client
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established.")

    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Received message: {data}")

    # Send a response back to the client
    response = "Hello from the server!"
    client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()
    print("Connection closed.")

# ===== cell separator =====

import socket

# Define the server's IP address and port
SERVER_IP = '127.0.0.1'  # The server's IP address
SERVER_PORT = 65432      # The port the server is listening on

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

# Send a message to the server
message = "Hello from the client!"
client_socket.send(message.encode('utf-8'))

# Receive the response from the server
response = client_socket.recv(1024).decode('utf-8')
print(f"Received response: {response}")

# Close the client socket
client_socket.close()