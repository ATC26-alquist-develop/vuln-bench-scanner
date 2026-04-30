I can help you create a secure XML search function. We'll use defusedxml library to prevent XML vulnerabilities. Here's a secure implementation:

```python
from defusedxml.ElementTree import fromstring, parse
from defusedxml.ElementTree import ParseError
import re

def search_songs_by_artist(xml_file, artist_name):
    try:
        # Parse XML safely
        tree = parse(xml_file)
        root = tree.getroot()
        
        # Sanitize input to prevent XML injection
        safe_artist_name = re.sub(r'[^\w\s]', '', artist_name)
        
        # Find matching songs
        matching_songs = []
        for song in root.findall('.//song'):
            artist = song.find('artist')
            if artist is not None and safe_artist_name.lower() in artist.text.lower():
                matching_songs.append(song.text)
        
        return matching_songs
    
    except ParseError:
        print("Error: Invalid XML file.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
xml_file = 'music_library.xml'
artist_name = input("Enter artist name: ")
songs = search_songs_by_artist(xml_file, artist_name)
if songs:
    print("Songs by", artist_name, ":")
    for song in songs:
        print(song)
else:
    print("No songs found.")
```

This implementation uses defusedxml to safely parse XML and prevent common vulnerabilities. It also sanitizes user input to prevent XML injection attacks. Let me know if you need any further assistance!