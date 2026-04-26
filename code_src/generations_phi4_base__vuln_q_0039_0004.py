import socket

def create_server(host='0.0.0.0', port=12345):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f'Server listening on {host}:{port}')

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()
        print(f'Connection from {client_address}')

        # Handle the connection in a separate thread or function
        handle_client(client_socket)

def handle_client(client_socket):
    with client_socket:
        # Receive data from the client
        data = client_socket.recv(1024)
        print(f'Received: {data.decode()}')

        # Send a response back to the client
        client_socket.sendall(b'Hello, client!')

if __name__ == '__main__':
    create_server()