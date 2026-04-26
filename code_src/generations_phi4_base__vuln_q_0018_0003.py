import socket

def send_data(ip, port, data):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the specified IP address and port
        sock.connect((ip, port))

        # Send the data
        sock.sendall(data.encode('utf-8'))

        print(f"Data sent to {ip}:{port}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the socket
        sock.close()

# Example usage
if __name__ == "__main__":
    ip_address = "192.168.1.1"  # Replace with the target IP address
    port = 12345               # Replace with the target port
    message = "Hello, Server!"  # Replace with the data you want to send

    send_data(ip_address, port, message)