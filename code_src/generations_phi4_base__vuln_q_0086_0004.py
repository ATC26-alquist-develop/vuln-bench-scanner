import socket

def start_server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_address = ('0.0.0.0', 12345)  # Bind to all interfaces on port 12345
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)

    print(f"Server is listening on {server_address}")

    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection from {client_address}")

            # Receive the data in small chunks and send it back
            while True:
                data = connection.recv(1024)
                if data:
                    print(f"Received {data.decode()}")
                    connection.sendall(data)
                else:
                    break
        finally:
            # Clean up the connection
            connection.close()

if __name__ == "__main__":
    start_server()