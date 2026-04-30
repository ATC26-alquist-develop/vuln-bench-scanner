import os
import logging
from aws_cdk import core, aws_s3 as s3
from aws_cdk import aws_kms as kms
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Generate a secure encryption key
        encryption_key = kms.Key(self, "EncryptionKey",
                                description="Key for encrypting S3 bucket data",
                                generate_new_key=True)
        
        # Create S3 bucket with server-side encryption
        self.bucket = s3.Bucket(self, id=bucket_name,
                               encryption=s3.BucketEncryption.S3_MANAGED,
                               encryption_key=encryption_key,
                               block_public_acls=True,
                               block_public_policy=True,
                               object_encryption_configuration=s3.ObjectEncryption.S3_MANAGED,
                               removal_policy=core.RemovalPolicy.DESTROY)
        
        # Set secure permissions
        self.bucket.add_to_resource_policy(core.RemovalPolicy.from_cloud_formation_arns(
            "arn:aws:s3:::*"
        ))

    def generate_secure_key(self):
        """Generate a secure encryption key using cryptography library."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096
        )
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem

    def encrypt_data(self, plaintext: bytes) -> bytes:
        """Encrypt data using the generated key."""
        private_key = rsa.import_key(self.encryption_key.key_material)
        ciphertext = private_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    def decrypt_data(self, ciphertext: bytes) -> bytes:
        """Decrypt data using the generated key."""
        private_key = rsa.import_key(self.encryption_key.key_material)
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext