import socket

def create_and_close_socket():
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to a server (replace 'example.com' and 80 with your target)
        sock.connect(('example.com', 80))
        
        # Send some data (replace 'GET / HTTP/1.1\r\n\r\n' with your data)
        sock.sendall(b'GET / HTTP/1.1\r\n\r\n')
        
        # Receive data (replace 1024 with your expected buffer size)
        data = sock.recv(1024)
        
        # Process received data here
        print(data)
        
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        # Ensure the socket is closed
        if 'sock' in locals():
            sock.close()

if __name__ == "__main__":
    create_and_close_socket()