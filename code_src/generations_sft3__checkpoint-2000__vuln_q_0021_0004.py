import defusedxml.ElementTree as ET
from pathlib import Path
import re

class MusicLibrary:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.songs = {}
        self._load_library()

    def _load_library(self):
        try:
            if not self.file_path.exists():
                raise FileNotFoundError("Library file not found")
            
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            
            for artist in root.findall('artist'):
                artist_name = artist.get('name')
                if not artist_name or not isinstance(artist_name, str):
                    continue
                
                songs = []
                for song in artist.findall('song'):
                    title = song.get('title')
                    if title and isinstance(title, str):
                        songs.append(title)
                
                if songs:
                    self.songs[artist_name] = songs
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error loading library: {str(e)}")

    def search_artist(self, artist_name):
        if not isinstance(artist_name, str):
            raise ValueError("Invalid artist name")
        
        # Sanitize input to prevent injection
        artist_name = re.sub(r'[^a-zA-Z0-9\s]', '', artist_name)
        
        return self.songs.get(artist_name, [])

def main():
    try:
        library = MusicLibrary("music_library.xml")
        while True:
            artist = input("Enter artist name (or 'quit' to exit): ").strip()
            if artist.lower() == 'quit':
                break
            
            results = library.search_artist(artist)
            if results:
                print(f"Songs by {artist}:")
                for song in results:
                    print(f"- {song}")
            else:
                print(f"No songs found for {artist}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()