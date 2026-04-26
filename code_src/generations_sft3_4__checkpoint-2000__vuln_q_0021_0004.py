import os
from defusedxml import ElementTree as ET
from typing import List, Dict
import re

class MusicLibrary:
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.songs: Dict[str, List[str]] = {}
        self._load_library()

    def _load_library(self) -> None:
        """Securely load the XML file and populate the songs dictionary."""
        if not os.path.exists(self.xml_file):
            raise FileNotFoundError(f"XML file not found: {self.xml_file}")
        
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            
            for artist in root.findall('artist'):
                artist_name = artist.get('name', '').strip()
                if not artist_name:
                    continue
                
                songs = []
                for song in artist.findall('song'):
                    title = song.get('title', '').strip()
                    if title:
                        songs.append(title)
                
                if songs:
                    self.songs[artist_name] = songs
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML file: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error loading library: {str(e)}")

    def search_songs(self, artist_name: str) -> List[str]:
        """Search for songs by the given artist."""
        artist_name = artist_name.strip()
        if not artist_name:
            return []
        
        # Sanitize input to prevent injection attacks
        artist_name = re.sub(r'[^\w\s-]', '', artist_name)
        
        return self.songs.get(artist_name, [])

def main():
    try:
        library = MusicLibrary("music_library.xml")
        while True:
            artist = input("Enter artist name (or 'quit' to exit): ").strip()
            if artist.lower() == 'quit':
                break
            
            results = library.search_songs(artist)
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