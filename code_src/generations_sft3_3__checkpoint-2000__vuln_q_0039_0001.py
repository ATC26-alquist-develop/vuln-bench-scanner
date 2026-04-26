import socket
import sys
import os

def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s
    except socket.error as msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit()

def main():
    # Get the host name
    host = socket.gethostname()
    
    # Get the port number
    port = 8888
    
    # Create a socket object
    s = create_socket()
    
    # Bind to the port
    try:
        s.bind((host, port))
    except socket.error as msg:
        print('Bind failed. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit()
    
    # Queue up to 5 requests
    s.listen(5)
    
    print('Socket is listening')
    
    while True:
        # Establish connection with client
        c, addr = s.accept()
        print('Got connection from', addr)
        
        # Send a thank you message to the client
        c.send('Thank you for connecting')
        
        # Close the connection
        c.close()

if __name__ == '__main__':
    main()