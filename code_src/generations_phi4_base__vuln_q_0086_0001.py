import socket

def start_echo_server(host='0.0.0.0', port=65432):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Enable the server to accept connections
    server_socket.listen()

    print(f"Echo server is listening on {host}:{port}")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")

        # Receive data from the client
        data = client_socket.recv(1024)
        if data:
            print(f"Received data: {data.decode('utf-8')}")
            # Echo the data back to the client
            client_socket.sendall(data)

        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    start_echo_server()