import socket

def start_echo_server(host='0.0.0.0', port=8080):
    # Create a socket object using IPv4 and TCP protocol
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Echo server is listening on {host}:{port}")
    
    try:
        while True:
            # Accept a connection
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            
            # Receive data from the client
            data = client_socket.recv(1024)
            
            # If no data is received, it means the client has closed the connection
            if not data:
                break
            
            # Echo the received data back to the client
            client_socket.sendall(data)
            
            # Close the client socket
            client_socket.close()
    finally:
        # Close the server socket
        server_socket.close()
        print("Echo server is shut down.")

if __name__ == "__main__":
    start_echo_server()