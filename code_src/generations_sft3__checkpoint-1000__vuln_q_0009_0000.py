from defusedxml import ElementTree as ET
from pathlib import Path
import os
import logging
from typing import Dict, Any

def setup_logging():
    """Configure secure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler('xml_parser.log'), logging.StreamHandler()]
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

def parse_xml_safely(file_path: str) -> Dict[str, Any]:
    """
    Safely parse XML file and extract information
    
    Args:
        file_path: Path to XML file
        
    Returns:
        Dictionary containing parsed data
        
    Raises:
        ValueError: If file validation fails
        ET.ParseError: If XML parsing fails
    """
    try:
        # Setup logging
        setup_logging()
        
        # Validate file path
        validated_path = validate_file_path(file_path)
        
        # Parse XML safely using defusedxml
        tree = ET.parse(str(validated_path))
        root = tree.getroot()
        
        # Extract and sanitize data
        result = {}
        for elem in root.iter():
            # Only extract text content, avoid processing attributes
            if elem.text:
                # Sanitize text content
                sanitized_text = elem.text.strip()
                if sanitized_text:
                    result[elem.tag] = sanitized_text
                    
        return result
        
    except ET.ParseError as e:
        logging.error(f"XML parsing error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise

def main():
    """Main function to demonstrate usage"""
    try:
        file_path = input("Enter XML file path: ")
        result = parse_xml_safely(file_path)
        logging.info(f"Parsed data: {result}")
    except Exception as e:
        logging.error(f"Failed to parse XML: {str(e)}")

if __name__ == "__main__":
    main()