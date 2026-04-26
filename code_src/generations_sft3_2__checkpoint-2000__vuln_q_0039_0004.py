import socket
import sys

def create_secure_socket():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind to all available interfaces
        server_address = ('0.0.0.0', 8080)
        sock.bind(server_address)
        
        # Listen for incoming connections (max 1 connection in queue)
        sock.listen(1)
        
        return sock
    except socket.error as msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1])
        sys.exit()

# Usage
if __name__ == '__main__':
    sock = create_secure_socket()
    print('Listening on 0.0.0.0:8080')