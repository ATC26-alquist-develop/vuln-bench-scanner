import socket

def connect_to_server(server_ip, server_port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((server_ip, server_port))
    
    try:
        # Send data to the server
        message = "Hello, server!"
        client_socket.sendall(message.encode())
        
        # Receive data from the server
        response = client_socket.recv(1024)
        print(f"Received from server: {response.decode()}")
        
    finally:
        # Close the connection
        client_socket.close()

# Replace with the actual server IP and port
server_ip = '192.168.1.100'  # Example IP address
server_port = 12345          # Example port number

connect_to_server(server_ip, server_port)