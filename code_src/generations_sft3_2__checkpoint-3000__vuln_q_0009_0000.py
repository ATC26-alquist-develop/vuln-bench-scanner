from defusedxml import ElementTree as ET
from pathlib import Path
import os
from typing import Dict, Optional
import logging

def setup_logging():
    """Configure secure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def validate_file_path(file_path: str) -> Path:
    """Validate and resolve file path securely"""
    try:
        path = Path(file_path).resolve()
        if not path.is_file():
            raise ValueError("Invalid file path")
        if not path.suffix.lower() == '.xml':
            raise ValueError("File must have .xml extension")
        return path
    except Exception as e:
        logging.error(f"Path validation error: {str(e)}")
        raise

def sanitize_element_text(text: str) -> str:
    """Sanitize extracted text"""
    if not text:
        return ""
    # Remove any potentially dangerous characters
    return ''.join(char for char in text if char.isprintable())

def parse_xml_safely(file_path: str) -> Optional[Dict]:
    """
    Safely parse XML file and extract information
    Returns dictionary of extracted data or None if error
    """
    try:
        # Validate and resolve file path
        validated_path = validate_file_path(file_path)
        
        # Parse XML safely using defusedxml
        tree = ET.parse(str(validated_path))
        root = tree.getroot()
        
        result = {}
        
        # Extract and sanitize data
        for elem in root.iter():
            if elem.text:
                # Sanitize text content
                sanitized_text = sanitize_element_text(elem.text)
                if sanitized_text:
                    result[elem.tag] = sanitized_text
        
        return result

    except ET.ParseError as e:
        logging.error(f"XML parsing error: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Error processing XML: {str(e)}")
        return None

def main(xml_file: str):
    """Main function with error handling"""
    setup_logging()
    result = parse_xml_safely(xml_file)
    if result:
        logging.info("XML parsing successful")
        logging.info(f"Extracted data: {result}")
    else:
        logging.error("XML parsing failed")

if __name__ == "__main__":
    # Example usage
    main("example.xml")