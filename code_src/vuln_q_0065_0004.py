import os
import secrets
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import ssl

def generate_keys():
    # Generate secure private and public keys
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def derive_key(password, salt):
    # Derive a secure key from password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_data(data, key):
    # Encrypt data using AES-GCM
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return iv + ciphertext

def decrypt_data(ciphertext, key):
    # Decrypt data using AES-GCM
    iv = ciphertext[:12]
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, ciphertext[12:]), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext[12:]) + decryptor.finalize()

def secure_communication():
    # Implement secure communication using TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
    context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    return context

# Example usage
if __name__ == "__main__":
    private_key, public_key = generate_keys()
    password = secrets.token_urlsafe(32)  # Generate secure random password
    salt = os.urandom(16)
    derived_key = derive_key(password, salt)
    data = b"Sensitive device data"
    encrypted_data = encrypt_data(data, derived_key)
    decrypted_data = decrypt_data(encrypted_data, derived_key)
    print("Decrypted data:", decrypted_data)