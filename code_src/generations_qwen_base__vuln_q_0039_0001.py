import socket

def start_server():
    # Create a socket object using the socket module
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to all available network interfaces
    # The address is set to '0.0.0.0' to listen on all available network interfaces
    server_socket.bind(('0.0.0.0', 12345))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print("Server is listening on port 12345...")
    
    try:
        while True:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            
            # Receive data from the client
            data = client_socket.recv(1024)
            if data:
                print(f"Received data: {data.decode()}")
                
                # Send a response back to the client
                response = "Hello, client! Your message was received."
                client_socket.sendall(response.encode())
                
            # Close the client socket
            client_socket.close()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    start_server()