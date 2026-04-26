import bcrypt

   # Generate a salt
   salt = bcrypt.gensalt()

   # Hash the password
   hashed_password = bcrypt.hashpw(b"your_password", salt)

   # Print the hashed password
   print(hashed_password)

# ===== cell separator =====

# Verify the password
   if bcrypt.checkpw(b"your_password", hashed_password):
       print("Password is correct!")
   else:
       print("Password is incorrect!")

# ===== cell separator =====

import hashlib

# Hash the password
hashed_password = hashlib.sha256(b"your_password").hexdigest()

# Print the hashed password
print(hashed_password)

# Verify the password
def verify_password(hashed_password, password):
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password

# Example verification
print(verify_password(hashed_password, b"your_password"))  # Should print True
print(verify_password(hashed_password, b"wrong_password"))  # Should print False