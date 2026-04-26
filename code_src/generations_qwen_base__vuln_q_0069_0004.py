import hashlib

def md5_hash(message):
    """
    Generate an MD5 hash for a given message.

    :param message: The message to hash.
    :return: The MD5 hash of the message.
    """
    # Create an MD5 hash object
    hash_object = hashlib.md5()
    
    # Update the hash object with the bytes of the message
    hash_object.update(message.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return hash_object.hexdigest()

def verify_message_integrity(message, expected_hash):
    """
    Verify the integrity of a message using its MD5 hash.

    :param message: The message to hash.
    :param expected_hash: The expected MD5 hash of the message.
    :return: True if the message's hash matches the expected hash, False otherwise.
    """
    # Generate the MD5 hash of the message
    actual_hash = md5_hash(message)
    
    # Compare the actual hash with the expected hash
    return actual_hash == expected_hash

# Example usage
message = "Hello, world!"
expected_hash = "65a8e27d8879283831b664bd8b7f0ad4"

# Verify the message integrity
is_integrity_verified = verify_message_integrity(message, expected_hash)

print(f"Message integrity verified: {is_integrity_verified}")