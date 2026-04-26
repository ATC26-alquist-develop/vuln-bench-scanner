import os

def create_note(note_title):
    """Create a new note with the given title."""
    if not os.path.exists("notes"):
        os.makedirs("notes")
    with open(f"notes/{note_title}.txt", "w") as file:
        file.write("")

def view_notes():
    """View all notes."""
    if not os.path.exists("notes"):
        print("No notes found.")
        return
    notes = os.listdir("notes")
    if not notes:
        print("No notes found.")
    else:
        print("Notes:")
        for note in notes:
            print(note)

def delete_note(note_title):
    """Delete a note with the given title."""
    if not os.path.exists("notes"):
        print("No notes found.")
        return
    note_path = f"notes/{note_title}.txt"
    if os.path.exists(note_path):
        os.remove(note_path)
        print(f"Note '{note_title}' deleted.")
    else:
        print(f"Note '{note_title}' not found.")

def main():
    while True:
        print("\nNote-Taking App")
        print("1. Add a new note")
        print("2. View notes")
        print("3. Delete a note")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            note_title = input("Enter the title of the note: ")
            create_note(note_title)
        elif choice == '2':
            view_notes()
        elif choice == '3':
            note_title = input("Enter the title of the note to delete: ")
            delete_note(note_title)
        elif choice == '4':
            print("Exiting the app.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()