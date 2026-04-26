import socket

# Define the port on which you want to listen
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_socket.bind(('0.0.0.0', PORT))

# Listen for incoming connections
server_socket.listen()

print(f"Server is listening on port {PORT}...")

# Accept connections
while True:
    client_socket, addr = server_socket.accept()
    print(f"Got a connection from {addr}")
    
    # Receive data from the client
    data = client_socket.recv(1024)
    print(f"Received data: {data.decode()}")

    # Send a response back to the client
    response = "Hello, client! Your message was received."
    client_socket.send(response.encode())
    
    # Close the client socket
    client_socket.close()

# ===== cell separator =====

import socket

# Define the server's IP address and port
SERVER_IP = '0.0.0.0'
PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, PORT))

# Send a message to the server
message = "Hello, server!"
client_socket.send(message.encode())

# Receive the response from the server
response = client_socket.recv(1024)
print(f"Received response: {response.decode()}")

# Close the client socket
client_socket.close()