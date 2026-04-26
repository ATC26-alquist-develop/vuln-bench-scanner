import boto3

# Configure your AWS credentials
aws_access_key_id = 'YOUR_ACCESS_KEY'
aws_secret_access_key = 'YOUR_SECRET_KEY'
region_name = 'YOUR_REGION'

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# ===== cell separator =====

kms_client = session.client('kms')

# ===== cell separator =====

new_key_alias = 'alias/new-encryption-key'
old_key_alias = 'alias/old-encryption-key'

# ===== cell separator =====

new_key = kms_client.create_key(
    Description='New encryption key for large dataset'
)
new_key_id = new_key['KeyMetadata']['KeyId']

# ===== cell separator =====

kms_client.update_alias(
    Alias=new_key_alias,
    TargetKeyId=new_key_id
)

# ===== cell separator =====

kms_client.update_alias(
    Alias=old_key_alias,
    TargetKeyId=new_key_id
)

# ===== cell separator =====

import base64

def encrypt_file(file_path, key_id):
    kms_client = session.client('kms')
    with open(file_path, 'rb') as file:
        plaintext = file.read()
        ciphertext = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext
        )
        return base64.b64encode(ciphertext['CiphertextBlob'])

encrypted_data = encrypt_file('path/to/your/large_dataset', new_key_id)