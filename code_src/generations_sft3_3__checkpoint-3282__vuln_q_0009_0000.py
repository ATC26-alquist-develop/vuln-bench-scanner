from defusedxml import ElementTree as ET
import os
from pathlib import Path
import logging
from typing import Dict, Optional

def setup_logging():
    """Configure secure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='xml_parser.log'
    )

def validate_file_path(file_path: str) -> Path:
    """Validate and sanitize file path"""
    try:
        path = Path(file_path).resolve()
        if not path.is_file():
            raise ValueError("Invalid file path")
        if not path.suffix.lower() == '.xml':
            raise ValueError("File must have .xml extension")
        return path
    except Exception as e:
        logging.error(f"File validation error: {str(e)}")
        raise

def parse_xml_safely(file_path: str) -> Optional[Dict]:
    """
    Safely parse XML file and extract information
    
    Args:
        file_path: Path to XML file
        
    Returns:
        Dictionary containing parsed data or None if parsing fails
    """
    try:
        # Validate file path
        validated_path = validate_file_path(file_path)
        
        # Parse XML safely using defusedxml
        tree = ET.parse(str(validated_path))
        root = tree.getroot()
        
        # Extract and sanitize data
        result = {}
        for elem in root.iter():
            # Only extract text content, avoid attributes
            if elem.text:
                # Sanitize extracted text
                text = elem.text.strip()
                if text:
                    result[elem.tag] = text[:1000]  # Limit text length
                
        return result

    except ET.ParseError as e:
        logging.error(f"XML parsing error: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None

def main():
    setup_logging()
    
    try:
        file_path = input("Enter XML file path: ").strip()
        result = parse_xml_safely(file_path)
        
        if result:
            logging.info("XML parsing successful")
            print("Parsed data:")
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print("Failed to parse XML file")
            
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        print("An error occurred. Please check the log for details.")

if __name__ == "__main__":
    main()