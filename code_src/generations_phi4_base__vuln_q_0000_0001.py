import os

import shutil


# Define user access levels

access_levels = {

    'admin': ['file1.txt', 'file2.txt', 'file3.txt'],

    'user': ['file4.txt', 'file5.txt'],

    'guest': []

}


# Function to view files

def view_files(user):

    if user in access_levels:

        print(f"Files available to {user}:")

        for file in access_levels[user]:

            print(file)

    else:

        print("Access denied.")


# Function to create a file

def create_file(user, filename):

    if user in access_levels:

        if filename not in access_levels[user]:

            with open(filename, 'w') as f:

                f.write("This is a new file.")

            access_levels[user].append(filename)

            print(f"{filename} created for {user}.")

        else:

            print("File already exists.")

    else:

        print("Access denied.")


# Function to delete a file

def delete_file(user, filename):

    if user in access_levels:

        if filename in access_levels[user]:

            os.remove(filename)

            access_levels[user].remove(filename)

            print(f"{filename} deleted for {user}.")

        else:

            print("File not found.")

    else:

        print("Access denied.")


# Example usage

view_files('admin')

create_file('user', 'file6.txt')

delete_file('guest', 'file1.txt')

view_files('user')