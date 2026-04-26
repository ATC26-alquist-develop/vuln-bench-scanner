import socket

def create_socket_and_close():
    # Define the server's IP address and port
    server_ip = '127.0.0.1'  # localhost
    server_port = 12345      # A specific port number

    # Create a socket object using the socket module
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created successfully.")

        # Connect the socket to the server's IP and port
        server_address = (server_ip, server_port)
        sock.connect(server_address)
        print(f"Socket connected to {server_address}")

        # Send data to the server
        message = "Hello, server!"
        sock.sendall(message.encode())

        # Receive data from the server
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print(f"Received: {data.decode()}")

    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket
        sock.close()
        print("Socket closed.")

if __name__ == "__main__":
    create_socket_and_close()