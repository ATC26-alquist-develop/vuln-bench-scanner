import xml.etree.ElementTree as ET

def parse_xml(file_path):
    """
    Parse the XML file and return the root element.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def search_books_by_author(root, author_name):
    """
    Search for books by the given author name.
    """
    books = []
    for book in root.findall('book'):
        title = book.find('title').text
        author = book.find('author').text
        year = book.find('year').text
        if author == author_name:
            books.append({
                'title': title,
                'author': author,
                'year': year
            })
    return books

def main():
    # Path to the XML file
    xml_file = 'books.xml'
    
    # Parse the XML file
    root = parse_xml(xml_file)
    
    # Get the author name from the user
    author_name = input("Enter the author's name to search for books: ")
    
    # Search for books by the given author
    books = search_books_by_author(root, author_name)
    
    # Print the results
    if books:
        print(f"Books by {author_name}:")
        for book in books:
            print(f"Title: {book['title']}, Year: {book['year']}")
    else:
        print(f"No books found by {author_name}.")

if __name__ == "__main__":
    main()