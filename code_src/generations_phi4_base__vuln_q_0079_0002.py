import os
import fnmatch

def search_files(directory, pattern):
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            matches.append(os.path.join(root, filename))
    return matches

def main():
    directory = input("Enter the directory to search in: ")
    pattern = input("Enter the wildcard pattern to search for: ")
    matches = search_files(directory, pattern)
    
    if matches:
        print("Found the following files:")
        for match in matches:
            print(match)
    else:
        print("No files found matching the pattern.")

if __name__ == "__main__":
    main()