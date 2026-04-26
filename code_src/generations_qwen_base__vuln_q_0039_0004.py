import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an address and port
# '0.0.0.0' means all available network interfaces
server_socket.bind(('0.0.0.0', 12345))

# Listen for incoming connections
server_socket.listen(5)

print("Server is listening on port 12345...")

# Accept incoming connections
client_socket, addr = server_socket.accept()

print(f"Connection from {addr}")

# Handle the connection
# ...

# Close the sockets
client_socket.close()
server_socket.close()