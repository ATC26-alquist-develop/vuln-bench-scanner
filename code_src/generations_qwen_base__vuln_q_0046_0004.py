import boto3
import time

# Initialize a session using your default AWS credentials
session = boto3.Session()

# Initialize a KMS client
kms_client = session.client('kms')

# ===== cell separator =====

# Get the key ID and key version ID
key_id = 'your-key-id'
key_version_id = 'your-key-version-id'

# Get the key metadata
response = kms_client.describe_key(KeyId=key_id)
current_key_version_id = response['KeyMetadata']['KeyVersionId']
print(f"Current Key Version ID: {current_key_version_id}")

# ===== cell separator =====

# Create a new key version
response = kms_client.create_key(
    Description='New Key Version for Large Dataset',
    KeyUsage='ENCRYPT_DECRYPT',
    Origin='AWS_KMS',
    Policy='{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"AWS": "*"}, "Action": "kms:*", "Resource": "*"}]}'
)

new_key_id = response['KeyMetadata']['KeyId']
new_key_version_id = response['KeyMetadata']['KeyVersionId']
print(f"New Key Version ID: {new_key_version_id}")

# Attach the new key version to the existing key
response = kms_client.attach_key(
    KeyId=key_id,
    TargetKeyId=new_key_id,
    TargetKeyVersionId=new_key_version_id
)
print("New Key Version Attached Successfully")

# ===== cell separator =====

# Encrypt the data with the new key
import base64

# Your data in base64 format
data = b'Your data here'
encrypted_data = kms_client.encrypt(
    KeyId=key_id,
    Plaintext=data
)

# Decrypt the data with the old key
decrypted_data = kms_client.decrypt(
    CiphertextBlob=encrypted_data['CiphertextBlob'],
    KeyId=key_id,
    KeyVersionId=current_key_version_id
)

# Convert the decrypted data back to a string
decrypted_data_str = base64.b64decode(decrypted_data['Plaintext']).decode('utf-8')
print(f"Decrypted Data: {decrypted_data_str}")