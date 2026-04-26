import ssl
import socket
import certifi

def check_ssl_certificate(hostname, port=443):
    """
    Check the SSL certificate of a given hostname and port.
    
    :param hostname: The hostname of the website to check.
    :param port: The port number (default is 443 for HTTPS).
    :return: True if the certificate is valid, False otherwise.
    """
    context = ssl.create_default_context(cafile=certifi.where())
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            # Get the certificate
            cert = ssock.getpeercert()
            # Check if the certificate is valid
            if cert:
                return True
            else:
                return False

def main():
    hostname = input("Enter the hostname of the website to check: ")
    if check_ssl_certificate(hostname):
        print(f"The SSL certificate for {hostname} is valid.")
    else:
        print(f"The SSL certificate for {hostname} is not valid.")

if __name__ == "__main__":
    main()