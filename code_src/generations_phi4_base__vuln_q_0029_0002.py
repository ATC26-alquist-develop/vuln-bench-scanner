Certainly! Below is a simple shell script that takes a filename as input and displays its contents using the `cat` command. This script is designed for Unix-like operating systems, such as Linux or macOS.

```bash
#!/bin/bash

# Check if the user provided an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 filename"
    exit 1
fi

# Assign the first argument to a variable
FILENAME=$1

# Check if the file exists
if [ ! -f "$FILENAME" ]; then
    echo "File not found: $FILENAME"
    exit 1
fi

# Display the contents of the file using cat
echo "Displaying contents of $FILENAME:"
cat "$FILENAME"
```

To use this script:

1. Save it to a file, for example, `display_file.sh`.
2. Make the script executable by running `chmod +x display_file.sh` in your terminal.
3. Execute the script by passing a filename as an argument, like so: `./display_file.sh yourfile.txt`.

This script first checks if you've provided a filename as an argument. If not, it prints a usage message and exits. It then checks if the specified file exists. If the file exists, it uses the `cat` command to display its contents. If the file does not exist, it prints an error message.