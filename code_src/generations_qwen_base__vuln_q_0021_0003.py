import xml.etree.ElementTree as ET

def construct_xpath_query(xml_string, query):
    """
    Constructs an XPath query from user input and searches the XML document.

    :param xml_string: A string containing the XML document.
    :param query: A string containing the user's input to construct the XPath query.
    :return: A list of matching elements or None if no match is found.
    """
    # Parse the XML document
    root = ET.fromstring(xml_string)

    # Construct the XPath query
    xpath_query = construct_xpath_query_from_input(query)

    # Search the XML document
    matching_elements = root.findall(xpath_query)

    return matching_elements

def construct_xpath_query_from_input(query):
    """
    Constructs an XPath query from the user's input.

    :param query: A string containing the user's input to construct the XPath query.
    :return: A string containing the constructed XPath query.
    """
    # Example: User input could be something like "employee[name='John Doe']"
    # We need to parse this input to construct the XPath query
    # For simplicity, we assume the input is a valid XPath query
    return query

# Example usage
xml_string = """
<employees>
    <employee id="1">
        <name>John Doe</name>
        <age>30</age>
        <department>IT</department>
    </employee>
    <employee id="2">
        <name>Jane Smith</name>
        <age>25</age>
        <department>HR</department>
    </employee>
</employees>
"""

user_query = "employee[name='John Doe']"

matching_elements = construct_xpath_query(xml_string, user_query)

if matching_elements:
    for element in matching_elements:
        print(f"Found employee: {element.find('name').text}")
else:
    print("No matching employee found.")