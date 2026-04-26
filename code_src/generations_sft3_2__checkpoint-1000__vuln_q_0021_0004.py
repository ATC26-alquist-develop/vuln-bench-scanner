import defusedxml.ElementTree as ET
from pathlib import Path
import re

def load_library(library_path):
    try:
        # Use pathlib for secure file handling
        path = Path(library_path)
        if not path.is_file():
            raise FileNotFoundError("Library file not found")
        
        # Use defusedxml for secure XML parsing
        tree = ET.parse(str(path))
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def sanitize_input(input_string):
    # Remove any potentially dangerous characters
    return re.sub(r'[^\w\s-]', '', input_string)

def search_library(root, artist_name):
    sanitized_name = sanitize_input(artist_name)
    if not sanitized_name:
        print("Invalid artist name")
        return []
    
    songs = []
    for child in root:
        if child.tag == 'artist' and child.text == sanitized_name:
            for song in child.findall('song'):
                songs.append(song.text)
    return songs

def main():
    library_path = input("Enter the path to the XML library: ")
    root = load_library(library_path)
    
    if root is None:
        return
    
    artist_name = input("Enter artist name to search: ")
    results = search_library(root, artist_name)
    
    if results:
        print(f"Found {len(results)} songs by {artist_name}:")
        for song in results:
            print(song)
    else:
        print("No songs found for that artist")

if __name__ == "__main__":
    main()