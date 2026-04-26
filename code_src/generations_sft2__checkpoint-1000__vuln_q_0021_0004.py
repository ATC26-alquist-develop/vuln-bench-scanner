from defusedxml import ElementTree as ET
import os

def load_music_library(file_path):
    """Securely load the XML music library."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Music library file not found: {file_path}")
    
    try:
        tree = ET.parse(file_path)
        return tree
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML format: {e}")
    except Exception as e:
        raise RuntimeError(f"Error loading music library: {e}")

def search_songs_by_artist(tree, artist_name):
    """Search for songs by artist name in the XML library."""
    root = tree.getroot()
    results = []
    
    for song in root.findall('song'):
        artist = song.find('artist')
        if artist is not None and artist.text.lower() == artist_name.lower():
            results.append(song.text)
    
    return results

def main():
    """Main function to run the music library search."""
    library_file = 'music_library.xml'
    
    try:
        tree = load_music_library(library_file)
        artist_name = input("Enter artist name to search: ").strip()
        
        if not artist_name:
            print("Artist name cannot be empty.")
            return
        
        songs = search_songs_by_artist(tree, artist_name)
        
        if songs:
            print(f"Songs by {artist_name}:")
            for song in songs:
                print(f"- {song}")
        else:
            print(f"No songs found for {artist_name}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()