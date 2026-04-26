import socket
import sys
import os

def create_socket():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set socket options to allow reuse address and port
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock
    except socket.error as msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1])
        sys.exit()

def main():
    # Get the host name and port number
    host = socket.gethostname()
    port = 8888
    
    # Create socket
    sock = create_socket()
    
    try:
        # Bind the socket to a specific address and port
        sock.bind((host, port))
        
        # Listen for incoming connections (max 5 queued connections)
        sock.listen(5)
        
        print('Socket is listening...')
        
        while True:
            # Wait for a connection
            print('Waiting for a connection...')
            client, address = sock.accept()
            
            # Print connection information
            print('Connection from', address)
            
            # Close the connection when done
            client.close()
            
    except socket.error as msg:
        print('Socket error: ' + str(msg))
        sys.exit()
    
    finally:
        # Close the socket
        sock.close()

if __name__ == '__main__':
    main()