import ssl
import socket

def check_ssl_certificate(host, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            cert = ssock.getpeercert()
            return cert

host = 'www.example.com'
cert = check_ssl_certificate(host)

if cert:
    print(f"SSL certificate for {host} is valid.")
else:
    print(f"SSL certificate for {host} is invalid.")