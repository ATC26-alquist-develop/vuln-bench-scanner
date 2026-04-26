import socket

# Define the host and port
host = '0.0.0.0'  # Listen on all available network interfaces
port = 12345      # Choose a port number

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {host}:{port}")

# Accept connections
client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# Receive data from the client
data = client_socket.recv(1024).decode()
print(f"Received: {data}")

# Send a response back to the client
response = "Hello, client! Your message was received."
client_socket.send(response.encode())

# Close the connection
client_socket.close()
server_socket.close()

# ===== cell separator =====

import socket

# Define the host and port
host = 'server_ip'  # Replace with the IP address of the server
port = 12345        # The same port as the server

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))

# Send a message to the server
message = "Hello, server!"
client_socket.send(message.encode())

# Receive the response from the server
response = client_socket.recv(1024).decode()
print(f"Received from server: {response}")

# Close the connection
client_socket.close()