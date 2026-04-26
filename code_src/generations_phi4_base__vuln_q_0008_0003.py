import os


def create_note(title, content):

    # Create a unique filename for the note

    filename = f"{title.replace(' ', '_')}.txt"

    # Save the content to a file

    with open(filename, 'w') as file:

        file.write(content)


def main():

    while True:

        # Get the title and content of the note from the user

        title = input("Enter the title of your note: ")

        content = input("Enter the content of your note: ")


        # Create the note

        create_note(title, content)


        # Ask the user if they want to create another note

        another = input("Do you want to create another note? (yes/no): ")

        if another.lower() != 'yes':

            break


if __name__ == "__main__":

    main()