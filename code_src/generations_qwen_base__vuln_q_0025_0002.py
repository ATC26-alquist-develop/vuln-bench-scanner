import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Define the pinned certificates
pinned_certs = [
    'path/to/pinned/cert1.pem',
    'path/to/pinned/cert2.pem',
    # Add more pinned certificates as needed
]

# Load the pinned certificates
with open(pinned_certs[0], 'rb') as f:
    cert1 = f.read()
with open(pinned_certs[1], 'rb') as f:
    cert2 = f.read()

# Define the server URL and credentials
server_url = 'https://example.com'
username = 'your_username'
password = 'your_password'

# Create a session with pinned certificates
session = requests.Session()
session.verify = pinned_certs[0]  # Use the first pinned certificate as the default
session.cert = (pinned_certs[0], '')  # Use the first pinned certificate as the client certificate

# Send the request
response = session.get(server_url, auth=HTTPBasicAuth(username, password), verify=session.verify, cert=session.cert)

# Print the response
print(response.status_code)
print(response.text)