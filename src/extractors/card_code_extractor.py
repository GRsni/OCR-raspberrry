"""
Utility functions for extracting CIP codes from health insurance card images.

This module provides functions to:
1. Normalize pixel coordinates from card bounding boxes
2. Extract text from specific regions using OCR
3. Validate extracted codes using regex patterns
4. Identify community and return expected code locations
"""

import re
import cv2
import numpy as np
from typing import Dict, Tuple, List, Optional
from .card_code_coordinates import CARD_COORDINATES, GENERAL_RULES, SPECIAL_NOTES


class CardCodeExtractor:
    """Extract CIP-SNS and CIP-AUT codes from health insurance card images."""

    def __init__(self, image_path: str):
        """
        Initialize with an image file.
        
        Args:
            image_path: Path to the card image
        """
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Cannot read image: {image_path}")
        
        self.height, self.width = self.image.shape[:2]
        self.image_path = image_path

    def pixel_coords_from_percent(self, x_min: float, x_max: float, 
                                   y_min: float, y_max: float) -> Tuple[int, int, int, int]:
        """
        Convert percentage coordinates to pixel coordinates.
        
        Args:
            x_min, x_max, y_min, y_max: Percentage coordinates (0-100)
            
        Returns:
            Tuple of (x_min_px, y_min_px, x_max_px, y_max_px) in pixels
        """
        x_min_px = int(self.width * x_min / 100)
        x_max_px = int(self.width * x_max / 100)
        y_min_px = int(self.height * y_min / 100)
        y_max_px = int(self.height * y_max / 100)
        return x_min_px, y_min_px, x_max_px, y_max_px

    def extract_region(self, x_min: float, x_max: float, 
                      y_min: float, y_max: float) -> np.ndarray:
        """
        Extract a rectangular region from the image.
        
        Args:
            x_min, x_max, y_min, y_max: Percentage coordinates
            
        Returns:
            Cropped image region as numpy array
        """
        x_min_px, y_min_px, x_max_px, y_max_px = self.pixel_coords_from_percent(
            x_min, x_max, y_min, y_max
        )
        return self.image[y_min_px:y_max_px, x_min_px:x_max_px]

    def preprocess_region(self, region: np.ndarray) -> np.ndarray:
        """
        Preprocess image region for OCR (grayscale, threshold, denoise).
        
        Args:
            region: Image region as numpy array
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply threshold to get black text on white
        _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
        
        return thresh

    def extract_text_from_region(self, x_min: float, x_max: float,
                                y_min: float, y_max: float) -> str:
        """
        Extract text from a region using pytesseract.
        
        Args:
            x_min, x_max, y_min, y_max: Percentage coordinates
            
        Returns:
            Extracted text (normalized)
        """
        try:
            import pytesseract
        except ImportError:
            raise ImportError("pytesseract required. Install with: pip install pytesseract")
        
        region = self.extract_region(x_min, x_max, y_min, y_max)
        preprocessed = self.preprocess_region(region)
        
        # Extract text with OCR config for numbers and letters
        text = pytesseract.image_to_string(
            preprocessed,
            config='--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        )
        
        # Normalize: remove whitespace, uppercase, remove accents
        text = text.strip().upper()
        text = re.sub(r'[^A-Z0-9]', '', text)
        return text

    def normalize_text(self, text: str) -> str:
        """Normalize OCR text: uppercase, remove non-alphanumeric."""
        text = text.upper()
        text = re.sub(r'[^A-Z0-9]', '', text)
        return text

    def validate_code(self, text: str, pattern: str) -> bool:
        """
        Validate extracted text against expected pattern.
        
        Args:
            text: Extracted text
            pattern: Regex pattern from coordinates
            
        Returns:
            True if text matches pattern
        """
        return bool(re.match(pattern, text))

    def find_codes_in_community(self, community: str, 
                                variant_idx: int = 0) -> Dict[str, Optional[str]]:
        """
        Extract CIP-SNS and CIP-AUT from a specific community card variant.
        
        Args:
            community: Community name (must match CARD_COORDINATES key)
            variant_idx: Index of variant (default 0)
            
        Returns:
            Dict with 'cip_sns', 'cip_aut', 'confidence' keys
        """
        if community not in CARD_COORDINATES:
            raise ValueError(f"Unknown community: {community}")
        
        card_info = CARD_COORDINATES[community]
        if variant_idx >= len(card_info['variants']):
            raise ValueError(f"Variant {variant_idx} not available for {community}")
        
        variant = card_info['variants'][variant_idx]
        result = {
            'community': community,
            'variant': variant['name'],
            'cip_sns': None,
            'cip_aut': None,
            'cip_sns_confidence': 0.0,
            'cip_aut_confidence': 0.0,
        }
        
        # Extract CIP-SNS
        sns_info = variant.get('cip_sns')
        if sns_info:
            try:
                sns_text = self.extract_text_from_region(
                    sns_info['x_min'], sns_info['x_max'],
                    sns_info['y_min'], sns_info['y_max']
                )
                if self.validate_code(sns_text, sns_info['ocr_pattern']):
                    result['cip_sns'] = sns_text
                    result['cip_sns_confidence'] = 0.95
            except Exception as e:
                print(f"Error extracting CIP-SNS: {e}")
        
        # Extract CIP-AUT
        aut_info = variant.get('cip_aut')
        if aut_info:
            try:
                aut_text = self.extract_text_from_region(
                    aut_info['x_min'], aut_info['x_max'],
                    aut_info['y_min'], aut_info['y_max']
                )
                if self.validate_code(aut_text, aut_info['ocr_pattern']):
                    result['cip_aut'] = aut_text
                    result['cip_aut_confidence'] = 0.95
            except Exception as e:
                print(f"Error extracting CIP-AUT: {e}")
        
        return result

    def get_all_variants(self, community: str) -> List[Dict]:
        """Get all available variants for a community."""
        if community not in CARD_COORDINATES:
            raise ValueError(f"Unknown community: {community}")
        return CARD_COORDINATES[community]['variants']


def display_coordinates(community: str, variant_idx: int = 0):
    """
    Display coordinate information for debugging/visualization.
    
    Args:
        community: Community name
        variant_idx: Variant index
    """
    if community not in CARD_COORDINATES:
        print(f"Unknown community: {community}")
        return
    
    card = CARD_COORDINATES[community]
    variant = card['variants'][variant_idx]
    
    print(f"\n{community} - {variant['name']}")
    print(f"Structure: {card['structure']}")
    print(f"\nCIP-SNS:")
    sns = variant.get('cip_sns')
    if sns:
        print(f"  Box: ({sns['x_min']}-{sns['x_max']}% W, {sns['y_min']}-{sns['y_max']}% H)")
        print(f"  Pattern: {sns['ocr_pattern']}")
        print(f"  Color: {sns['color_hint']}")
        print(f"  Notes: {sns['notes']}")
    
    print(f"\nCIP-AUT:")
    aut = variant.get('cip_aut')
    if aut:
        print(f"  Box: ({aut['x_min']}-{aut['x_max']}% W, {aut['y_min']}-{aut['y_max']}% H)")
        print(f"  Pattern: {aut['ocr_pattern']}")
        print(f"  Color: {aut['color_hint']}")
        print(f"  Notes: {aut['notes']}")
    
    if community in SPECIAL_NOTES:
        print(f"\nSPECIAL NOTES: {SPECIAL_NOTES[community]}")


if __name__ == "__main__":
    import sys
    
    print("Card Code Extractor Utility")
    print("=" * 60)
    print("\nAvailable communities:")
    for i, comm in enumerate(sorted(CARD_COORDINATES.keys()), 1):
        print(f"  {i:2}. {comm}")
    
    print("\n\nExample usage:")
    print("  from card_code_extractor import CardCodeExtractor")
    print("  extractor = CardCodeExtractor('card_image.jpg')")
    print("  result = extractor.find_codes_in_community('Andalucía')")
    print("  print(result)")
    
    print("\n\nCoordinate reference:")
    print("  display_coordinates('Andalucía')")
