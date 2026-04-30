```python
import html
import re
from typing import Dict, List
import json
from pathlib import Path

class SecureGuestbook:
    def __init__(self, file_path: str = "guestbook.json"):
        self.file_path = Path(file_path)
        self.messages: Dict[str, str] = {}
        self.load_messages()

    def load_messages(self) -> None:
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.messages = data
                except json.JSONDecodeError:
                    # If file is corrupted, start with an empty message list
                    self.messages = {}

    def save_messages(self) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(self.messages, f, indent=2)

    def add_message(self, name: str, message: str) -> None:
        # Validate input
        if not self._validate_input(name) or not self._validate_input(message):
            raise ValueError("Invalid input")

        # Sanitize inputs
        name = html.escape(name)
        message = html.escape(message)

        # Add message to the dictionary
        self.messages[name] = message
        self.save_messages()

    def get_messages(self) -> List[str]:
        return list(self.messages.values())

    def _validate_input(self, input_str: str) -> bool:
        # Validate input to prevent injection attacks
        return bool(re.match(r'^[a-zA-Z0-9\s\-.,!?]+$', input_str))

def main():
    guestbook = SecureGuestbook()

    while True:
        print("\n1. Add message")
        print("2. View messages")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            message = input("Enter your message: ")
            try:
                guestbook.add_message(name, message)
                print("Message added successfully!")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '2':
            messages = guestbook.get_messages()
            if messages:
                print("\nGuestbook Messages:")
                for msg in messages:
                    print(f"- {msg}")
            else:
                print("No messages yet.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
```


This implementation addresses several security concerns:

1. Input validation: The `_validate_input` method uses a regular expression to ensure that only alphanumeric characters and a limited set of punctuation are allowed in names and messages.

2. Input sanitization: We use `html.escape()` to prevent XSS attacks by escaping special characters in user input.

3. File handling: We use `json` for serialization and deserialization, which is safer than using `pickle` or other potentially dangerous methods.

4. Error handling: We catch `JSONDecodeError` to handle corrupted files gracefully.

5. Type hinting: We use type hints to improve code readability and catch potential type-related errors early.

6. Secure file path: We use `pathlib.Path` for file operations, which is more secure than string manipulation.

7. No global variables: We encapsulate the guestbook functionality within a class, avoiding global state.

8. Limited functionality: The script only allows adding and viewing messages, reducing the attack surface.

This implementation provides a basic, secure guestbook without introducing vulnerabilities. However, for a production environment, you might want to consider additional security measures such as rate limiting, user authentication, and using a database instead of a JSON file for better scalability and security.