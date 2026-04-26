from defusedxml import ElementTree as ET
from pathlib import Path
import os
from typing import Dict, Any
import logging

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
            raise ValueError("File must be an XML file")
        return path
    except Exception as e:
        logging.error(f"File validation error: {str(e)}")
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
        # Validate file path
        validated_path = validate_file_path(file_path)
        
        # Limit file size to prevent DoS (adjust as needed)
        if validated_path.stat().st_size > 10_000_000:  # 10MB limit
            raise ValueError("File too large")
            
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
                    result[elem.tag] = text
                    
        return result
        
    except ET.ParseError as e:
        logging.error(f"XML parsing error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise

def main():
    try:
        setup_logging()
        file_path = input("Enter XML file path: ")
        result = parse_xml_safely(file_path)
        logging.info(f"Parsed {len(result)} elements from {file_path}")
        print("Parsed data:", result)
    except Exception as e:
        logging.error(f"Script execution error: {str(e)}")
        print("An error occurred. Please check the log for details.")

if __name__ == "__main__":
    main()