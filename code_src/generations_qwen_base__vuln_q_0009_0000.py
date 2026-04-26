import xml.etree.ElementTree as ET

    def parse_xml(file_path):
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract information from the XML
        for book in root.findall('book'):
            book_id = book.get('id')
            title = book.find('title').text
            author = book.find('author').text
            year = book.find('year').text

            # Print the extracted information
            print(f"Book ID: {book_id}")
            print(f"Title: {title}")
            print(f"Author: {author}")
            print(f"Year: {year}")
            print("-" * 40)

    # Specify the path to your XML file
    xml_file_path = 'data.xml'
    parse_xml(xml_file_path)