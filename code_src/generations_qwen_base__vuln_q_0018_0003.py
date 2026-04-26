import socket

def create_socket(ip_address, port):
    # Create a socket object
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Failed to create socket: {e}")
        return None
    
    # Connect to the server
    try:
        sock.connect((ip_address, port))
    except socket.error as e:
        print(f"Failed to connect to server: {e}")
        sock.close()
        return None
    
    return sock

def send_data(sock, data):
    if sock is None:
        print("Socket is not created or connected.")
        return
    
    try:
        sock.sendall(data.encode('utf-8'))
        print("Data sent successfully.")
    except socket.error as e:
        print(f"Failed to send data: {e}")
    finally:
        sock.close()

def main():
    ip_address = '127.0.0.1'  # Replace with the server's IP address
    port = 12345             # Replace with the server's port number
    data_to_send = "Hello, Server!"  # Data you want to send

    # Create and connect the socket
    sock = create_socket(ip_address, port)
    
    if sock is not None:
        # Send data
        send_data(sock, data_to_send)

if __name__ == "__main__":
    main()