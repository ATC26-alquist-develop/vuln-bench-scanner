import socket
import threading

def connect_and_send(server_ip, server_port, message):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        sock.connect((server_ip, server_port))
        
        # Send the message to the server
        sock.sendall(message.encode())
        
        # Receive the response from the server
        response = sock.recv(1024)
        print(f"Received from {server_ip}:{server_port}: {response.decode()}")
        
        # Close the socket
        sock.close()
    except Exception as e:
        print(f"Error connecting to {server_ip}:{server_port}: {e}")

def main():
    # List of servers to connect to
    servers = [
        ("192.168.1.100", 12345),  # Server 1
        ("192.168.1.101", 12346),  # Server 2
        ("192.168.1.102", 12347)   # Server 3
    ]
    
    # List of messages to send to each server
    messages = [
        "Hello Server 1",
        "Hello Server 2",
        "Hello Server 3"
    ]
    
    # Create threads for each server connection
    threads = []
    for server, message in zip(servers, messages):
        thread = threading.Thread(target=connect_and_send, args=(server[0], server[1], message))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()