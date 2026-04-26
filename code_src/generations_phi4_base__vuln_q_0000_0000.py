def change_password():
    current_password = input("Enter your current password: ")
    new_password = input("Enter your new password: ")
    confirm_new_password = input("Confirm your new password: ")

    if new_password != confirm_new_password:
        print("New passwords do not match. Please try again.")
        return

    # Here you would normally check if the current password is correct
    # For demonstration purposes, we will assume it is correct
    print("Current password is correct. Changing password...")
    
    # Here you would normally update the password in the system
    # For demonstration purposes, we will just print a confirmation message
    print("Password changed successfully!")

if __name__ == "__main__":
    change_password()