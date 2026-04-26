import getpass

def change_password(current_password, new_password):
    """
    Change the password in the system.
    
    :param current_password: The current password of the user.
    :param new_password: The new password to be set.
    """
    # Placeholder for actual password checking logic
    # In a real system, you would compare the current password with the stored password
    # and ensure it meets the complexity requirements.
    if current_password == "correct_current_password":
        if new_password == new_password_confirmation:
            print("Password changed successfully.")
            # Placeholder for updating the password in the system
            # In a real system, you would update the password in the database or file
            # and clear the temporary password storage.
        else:
            print("New password and confirmation do not match.")
    else:
        print("Incorrect current password.")

def main():
    print("Welcome to the Password Change System!")
    
    # Prompt the user to enter the current password
    current_password = getpass.getpass("Enter your current password: ")
    
    # Prompt the user to enter the new password
    new_password = getpass.getpass("Enter your new password: ")
    new_password_confirmation = getpass.getpass("Confirm your new password: ")
    
    # Check if the new password matches the confirmation
    if new_password == new_password_confirmation:
        change_password(current_password, new_password)
    else:
        print("New password and confirmation do not match. Please try again.")

if __name__ == "__main__":
    main()