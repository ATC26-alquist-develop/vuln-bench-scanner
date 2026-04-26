import socket

# List of server addresses and ports
servers = [
    ('127.0.0.1', 8080),
    ('127.0.0.1', 8081),
    ('127.0.0.1', 8082)
]

# Message to be sent to each server
message = "Hello, Server!"

# Function to establish a socket connection and send a message
def connect_and_send(server_address, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_address, port))
        s.sendall(message.encode())
        print(f"Sent message to {server_address}:{port}")

# Loop through the list of servers and establish connections
for server in servers:
    connect_and_send(server[0], server[1], message)