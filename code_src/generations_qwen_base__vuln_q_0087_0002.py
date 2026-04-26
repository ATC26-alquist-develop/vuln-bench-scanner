import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('localhost', 10000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print(f"Server listening on {server_address[0]}:{server_address[1]}")

while True:
    # Wait for a connection
    print("Waiting for a connection...")
    connection, client_address = server_socket.accept()
    try:
        print(f"Connection from {client_address}")

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print(f"Received: {data.decode()}")
            if data:
                print(f"Sending data back to the client")
                connection.sendall(data)
            else:
                print("No more data from", client_address)
                break
    finally:
        # Clean up the connection
        connection.close()

# ===== cell separator =====

import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('localhost', 10000)
client_socket.connect(server_address)

try:
    # Send data
    message = "Hello, Server!"
    print(f"Sending: {message}")
    client_socket.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = client_socket.recv(16)
        amount_received += len(data)
        print(f"Received: {data.decode()}")
finally:
    # Clean up the connection
    client_socket.close()