import socket
import sys
import os

def create_socket():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set socket options to allow multiple connections
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock
    except socket.error as msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1])
        sys.exit()

def bind_socket(sock):
    try:
        # Bind the socket to a specific address and port
        server_address = ('0.0.0.0', 8888)
        sock.bind(server_address)
        # Listen for incoming connections (max 1 queued connection)
        sock.listen(1)
        return sock
    except socket.error as msg:
        print('Bind failed. Error: ' + str(msg))
        sys.exit()

def accept_connections(sock):
    try:
        # Wait for a connection
        connection, client_address = sock.accept()
        print('Connection from ' + str(client_address))
        return connection, client_address
    except socket.error as msg:
        print('Accept failed. Error: ' + str(msg))
        sys.exit()

def main():
    # Create socket
    sock = create_socket()
    if sock is None:
        return
    
    # Bind socket
    sock = bind_socket(sock)
    if sock is None:
        return
    
    # Accept connections
    connection, client_address = accept_connections(sock)
    if connection is None:
        return
    
    try:
        # Receive data from client
        data = connection.recv(1024)
        if data:
            print('Received: ' + data.decode('utf-8'))
            # Send response
            connection.sendall(b'Hello, client!')
        else:
            print('No data received')
    except socket.error as msg:
        print('Error receiving data. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1])
    finally:
        # Clean up the connection
        connection.close()
        sock.close()

if __name__ == '__main__':
    main()