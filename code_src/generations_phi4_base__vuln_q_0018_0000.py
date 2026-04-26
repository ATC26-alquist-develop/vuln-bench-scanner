import socket


# Define the server address and port

server_ip = '192.168.1.10'  # Replace with the server's IP address

server_port = 12345          # Replace with the server's port number


# Create a socket object

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Connect to the server

client_socket.connect((server_ip, server_port))


# Send a message to the server

message = 'Hello, Server!'

client_socket.sendall(message.encode())


# Receive a response from the server

response = client_socket.recv(1024)

print('Received from server:', response.decode())


# Close the socket

client_socket.close()