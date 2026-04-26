import xml.etree.ElementTree as ET

def load_books_from_xml(file_path):
    """Load books from the XML file and return a list of book dictionaries."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    books = []
    for book in root.findall('book'):
        title = book.find('title').text
        author = book.find('author').text
        year = book.find('year').text
        books.append({'title': title, 'author': author, 'year': year})
    return books

def search_books_by_author(books, author_name):
    """Search for books by the given author name and return a list of matching books."""
    matching_books = [book for book in books if book['author'].lower() == author_name.lower()]
    return matching_books

def main():
    # Load books from the XML file
    books = load_books_from_xml('books.xml')
    
    # Get the author's name from the user
    author_name = input("Enter the author's name to search for books: ")
    
    # Search for books by the given author
    matching_books = search_books_by_author(books, author_name)
    
    # Display the results
    if matching_books:
        print(f"Books by {author_name}:")
        for book in matching_books:
            print(f"Title: {book['title']}, Year: {book['year']}")
    else:
        print(f"No books found by {author_name}.")

if __name__ == "__main__":
    main()