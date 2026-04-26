import xml.etree.ElementTree as ET

def search_songs_by_artist(artist_name, xml_file='music_library.xml'):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Find the artist by name
        artist = root.find(f".//artist[name='{artist_name}']")
        if artist is None:
            print(f"No artist found with the name '{artist_name}'.")
            return

        # Get the list of songs by the artist
        songs = artist.find('songs/song').text
        print(f"Songs by {artist_name}: {songs}")

    except ET.ParseError:
        print("Error parsing the XML file.")
    except FileNotFoundError:
        print(f"File '{xml_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    artist_name = input("Enter the artist name: ")
    search_songs_by_artist(artist_name)