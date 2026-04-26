import hashlib

def compute_md5(message):
    # Create an MD5 hash object
    md5_hash = hashlib.md5()
    
    # Update the hash object with the bytes of the message
    md5_hash.update(message.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return md5_hash.hexdigest()

# Example usage
if __name__ == "__main__":
    message = "Hello, World!"
    md5_result = compute_md5(message)
    print(f"MD5 hash of '{message}': {md5_result}")