import socket

def start_server(host='127.0.0.1', port=65432):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a public host, and a well-known port
    server_socket.bind((host, port))
    
    # Become a server socket
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        # Establish a connection
        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")
        
        # Receive data from the client
        data = client_socket.recv(1024)
        print(f"Received: {data.decode('utf-8')}")
        
        # Send a response back to the client
        response = "Hello, client! Thank you for connecting."
        client_socket.sendall(response.encode('utf-8'))
        
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start_server()

# ===== cell separator =====

import socket

def start_client(host='127.0.0.1', port=65432):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((host, port))
    
    # Send a message to the server
    message = "Hello, server!"
    client_socket.sendall(message.encode('utf-8'))
    
    # Receive the response from the server
    response = client_socket.recv(1024)
    print(f"Received: {response.decode('utf-8')}")
    
    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()