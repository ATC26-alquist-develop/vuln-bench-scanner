import socket

def create_socket_connection(host, port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect the socket to the port where the server is listening
        server_address = (host, port)
        print(f"Connecting to {host} port {port}")
        sock.connect(server_address)

        # Send data
        message = 'This is the message. It will be echoed back.'
        print(f"Sending: {message}")
        sock.sendall(message.encode())

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print(f"Received: {data.decode()}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing socket")
        sock.close()

# Replace 'localhost' and 10000 with the appropriate host and port
create_socket_connection('localhost', 10000)