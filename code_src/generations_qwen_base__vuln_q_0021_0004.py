import xml.etree.ElementTree as ET

def parse_xml(xml_file):
    """Parse the XML file and return a dictionary of artists and their songs."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    artists = {}

    for artist in root.findall('artist'):
        name = artist.get('name')
        songs = [song.get('title') for song in artist.findall('song')]
        artists[name] = songs

    return artists

def search_artist(artists, artist_name):
    """Search for an artist and return their songs."""
    if artist_name in artists:
        return artists[artist_name]
    else:
        return "No songs found for this artist."

def main():
    xml_file = 'music_library.xml'  # Path to your XML file
    artists = parse_xml(xml_file)

    while True:
        artist_name = input("Enter an artist name to find their songs (or 'exit' to quit): ")
        if artist_name.lower() == 'exit':
            break

        songs = search_artist(artists, artist_name)
        if isinstance(songs, list):
            print(f"Songs by {artist_name}:")
            for song in songs:
                print(f"- {song}")
        else:
            print(songs)

if __name__ == "__main__":
    main()