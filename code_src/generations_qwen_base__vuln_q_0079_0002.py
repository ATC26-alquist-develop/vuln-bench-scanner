import os
import fnmatch

def search_files(directory, pattern):
    """
    Search for files in the given directory that match the given pattern.
    
    :param directory: The directory to search in.
    :param pattern: The wildcard pattern to match files against.
    :return: A list of matching file paths.
    """
    matches = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                matches.append(os.path.join(root, name))
    return matches

def main():
    directory = input("Enter the directory to search: ")
    pattern = input("Enter the wildcard pattern to search for (e.g., '*.txt'): ")
    
    matches = search_files(directory, pattern)
    
    if matches:
        print(f"Found {len(matches)} matching files:")
        for match in matches:
            print(match)
    else:
        print("No matching files found.")

if __name__ == "__main__":
    main()