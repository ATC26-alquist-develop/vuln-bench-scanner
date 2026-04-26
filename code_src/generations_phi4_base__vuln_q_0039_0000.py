import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a public host and a port
server_socket.bind(('0.0.0.0', 8080))

# Enable the server to accept connections
server_socket.listen(5)

print("Server is listening on port 8080...")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} has been established.")

    # Send a welcome message to the client
    client_socket.send(b"Welcome to the server!")

    # Close the connection
    client_socket.close()