from defusedxml import ElementTree as ET
from pathlib import Path
import os
from typing import Dict, Optional
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

def parse_xml_safely(file_path: str) -> Optional[Dict]:
    """
    Safely parse XML file and extract information
    
    Args:
        file_path: Path to the XML file
        
    Returns:
        Dictionary containing parsed data or None if parsing fails
    """
    try:
        # Validate and resolve file path
        validated_path = validate_file_path(file_path)
        
        # Limit file size to prevent DoS (adjust as needed)
        if validated_path.stat().st_size > 10_000_000:  # 10MB limit
            logging.error("File too large")
            return None
            
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
        file_path = input("Enter XML file path: ")
        result = parse_xml_safely(file_path)
        
        if result:
            logging.info("XML parsing completed successfully")
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