import socket

def create_server_socket(host='0.0.0.0', port=12345):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to all available interfaces and a specific port
    server_socket.bind((host, port))
    
    # Listen for incoming connections (max 5 queued connections)
    server_socket.listen(5)
    
    return server_socket