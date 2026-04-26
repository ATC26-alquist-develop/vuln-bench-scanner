import socket

# Server code
def server():
    s = socket.socket()
    s.bind(('localhost', 12345))
    s.listen(5)
    print("Server started, waiting for connections...")
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        c.send(b'Hello, client!')
        c.close()

# Client code
def client():
    s = socket.socket()
    s.connect(('localhost', 12345))
    print(s.recv(1024))
    s.close()

if __name__ == '__main__':
    choice = input("Enter 'server' to run the server or 'client' to run the client: ")
    if choice == 'server':
        server()
    elif choice == 'client':
        client()