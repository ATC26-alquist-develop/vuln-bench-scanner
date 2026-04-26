import requests

import certifi


# Define the expected certificate or public key

EXPECTED_CERTIFICATE = '-----BEGIN CERTIFICATE-----\n...'

EXPECTED_PUBLIC_KEY = '...'


def verify_certificate(response):

    # Extract the certificate from the response

    cert = response.raw.connection.sock.getpeercert(binary_form=True)


    # Convert the certificate to a string

    cert_str = ssl.DER_cert_to_PEM_cert(cert)


    # Check if the certificate matches the expected one

    if cert_str != EXPECTED_CERTIFICATE:

        raise ValueError("Certificate pinning failed!")


# Use the requests library to make a request

response = requests.get('https://yourserver.com', verify=certifi.where())


# Perform the certificate pinning check

verify_certificate(response)