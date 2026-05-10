#!/usr/bin/env python3
"""
Quick Start Guide: Using Card Code Coordinates

This script demonstrates how to use the card_code_coordinates module
to identify CIP-SNS and CIP-AUT locations on Spanish health insurance cards.
"""

from card_code_coordinates import CARD_COORDINATES, GENERAL_RULES, SPECIAL_NOTES
from card_code_extractor import display_coordinates


def print_coordinate_summary():
    """Print a summary of all communities and their code locations."""
    print("\n" + "=" * 100)
    print("SPANISH HEALTH INSURANCE CARD CODE COORDINATE LOCATIONS")
    print("=" * 100)
    
    for community in sorted(CARD_COORDINATES.keys()):
        card_info = CARD_COORDINATES[community]
        variant = card_info['variants'][0]  # First variant
        
        cip_sns = variant.get('cip_sns', {})
        cip_aut = variant.get('cip_aut', {})
        
        print(f"\n{community}")
        print(f"  Structure: {card_info['structure']}")
        print(f"  CIP-SNS:   Box ({cip_sns.get('x_min', '?')}–{cip_sns.get('x_max', '?')}% W, " +
              f"{cip_sns.get('y_min', '?')}–{cip_sns.get('y_max', '?')}% H)  Pattern: {cip_sns.get('ocr_pattern', 'N/A')}")
        print(f"  CIP-AUT:   Box ({cip_aut.get('x_min', '?')}–{cip_aut.get('x_max', '?')}% W, " +
              f"{cip_aut.get('y_min', '?')}–{cip_aut.get('y_max', '?')}% H)  Pattern: {cip_aut.get('ocr_pattern', 'N/A')}")
        
        if community in SPECIAL_NOTES:
            print(f"  ⚠️  {SPECIAL_NOTES[community]}")


def print_usage_examples():
    """Print example code snippets for using the modules."""
    print("\n" + "=" * 100)
    print("USAGE EXAMPLES")
    print("=" * 100)
    
    print("""
1. VIEW COORDINATE REFERENCE FOR A SPECIFIC COMMUNITY
   ────────────────────────────────────────────────────
   from card_code_coordinates import CARD_COORDINATES
   
   # Get coordinates for Andalucía
   and_card = CARD_COORDINATES['Andalucía']
   variant = and_card['variants'][0]
   
   print(f"CIP-SNS location: {variant['cip_sns']}")
   print(f"CIP-AUT location: {variant['cip_aut']}")


2. EXTRACT CODES FROM AN IMAGE
   ────────────────────────────
   from card_code_extractor import CardCodeExtractor
   
   # Load an image
   extractor = CardCodeExtractor('card_photo.jpg')
   
   # Extract codes for a specific community
   result = extractor.find_codes_in_community('Navarra', variant_idx=0)
   
   print(f"Community: {result['community']}")
   print(f"CIP-SNS: {result['cip_sns']}")
   print(f"CIP-AUT: {result['cip_aut']}")


3. DISPLAY COORDINATE REFERENCE WITH DETAILS
   ──────────────────────────────────────────
   from card_code_extractor import display_coordinates
   
   # Show all details for a community
   display_coordinates('Comunidad Valenciana')
   
   # This prints:
   # - Full coordinate boxes
   # - Regex patterns for validation
   # - Color hints
   # - Special notes and warnings


4. CHECK IF CIP-AUT NEEDS LEADING ZEROS
   ────────────────────────────────────
   from card_code_coordinates import SPECIAL_NOTES
   
   community = 'Navarra'
   
   if community in SPECIAL_NOTES:
       print(SPECIAL_NOTES[community])
   # Output: "SI TECLEAR LOS CEROS INCLUIDOS AL PRINCIPIO DEL CIP-AUT (Type leading zeros)"
   
   # For País Vasco (different rule):
   # Output: "NO TECLEAR LOS CEROS INCLUIDOS AL PRINCIPIO DEL CIP-AUT (Do NOT type leading zeros)"


5. LIST ALL VARIANTS FOR A COMMUNITY
   ─────────────────────────────────
   from card_code_coordinates import CARD_COORDINATES
   
   community = 'Andalucía'
   variants = CARD_COORDINATES[community]['variants']
   
   for i, variant in enumerate(variants):
       print(f"Variant {i}: {variant['name']}")
""")


def print_coordinate_reference_table():
    """Print a compact table of all coordinates."""
    print("\n" + "=" * 100)
    print("COORDINATE REFERENCE TABLE (All Communities)")
    print("=" * 100)
    print(f"\n{'Community':<30} {'CIP-SNS Box (W%, H%)':<25} {'CIP-AUT Box (W%, H%)':<25}")
    print("-" * 100)
    
    for community in sorted(CARD_COORDINATES.keys()):
        card_info = CARD_COORDINATES[community]
        variant = card_info['variants'][0]
        
        cip_sns = variant.get('cip_sns', {})
        cip_aut = variant.get('cip_aut', {})
        
        sns_box = f"({cip_sns.get('x_min', '?')}-{cip_sns.get('x_max', '?')}, {cip_sns.get('y_min', '?')}-{cip_sns.get('y_max', '?')})"
        aut_box = f"({cip_aut.get('x_min', '?')}-{cip_aut.get('x_max', '?')}, {cip_aut.get('y_min', '?')}-{cip_aut.get('y_max', '?')})"
        
        print(f"{community:<30} {sns_box:<25} {aut_box:<25}")


def main():
    """Run all example outputs."""
    print("\n" + "╔" + "=" * 98 + "╗")
    print("║" + " " * 98 + "║")
    print("║" + "Spanish Health Insurance Card Code Coordinate Reference".center(98) + "║")
    print("║" + " " * 98 + "║")
    print("╚" + "=" * 98 + "╝")
    
    # Show summary
    print_coordinate_reference_table()
    
    # Show special cases
    print("\n" + "=" * 100)
    print("SPECIAL CASES & IMPORTANT NOTES")
    print("=" * 100)
    for community, note in sorted(SPECIAL_NOTES.items()):
        print(f"  • {community:30} → {note}")
    
    # Show usage examples
    print_usage_examples()
    
    # Full summary
    print_coordinate_summary()
    
    # File information
    print("\n" + "=" * 100)
    print("FILES INCLUDED")
    print("=" * 100)
    print("""
  1. card_code_coordinates.py
     └─ Complete dictionary with all communities and card variants
     └─ Normalized coordinates (0-100%) for all CIP-SNS and CIP-AUT locations
     └─ OCR patterns, color hints, and special notes
  
  2. card_code_extractor.py
     └─ CardCodeExtractor class for extracting codes from images
     └─ Image preprocessing and OCR integration
     └─ Coordinate conversion (% to pixels) and validation functions
  
  3. REFERENCE.md
     └─ Human-readable reference guide (markdown)
     └─ Detailed descriptions for each community
     └─ Data entry rules and special handling
  
  4. quick_start.py
     └─ This file (examples and usage guide)
""")
    
    print("\n" + "=" * 100)
    print("KEY FACTS")
    print("=" * 100)
    print(f"""
  ✓ Total communities covered:        20 (all autonomous communities + INGESA)
  ✓ Card variants tracked:            ~25 different physical card models
  ✓ CIP-SNS format:                   2 letters + 6 numbers (8 chars, always same format)
  ✓ CIP-AUT format:                   Variable by community (4-12 chars typically)
  ✓ Coordinate system:                Normalized 0-100 (independent of image resolution)
  ✓ Priority rule:                    Use CIP-SNS when available; fall back to CIP-AUT
  
  ⚠️  Special rules for data entry:
      • Navarra:          Type leading zeros in CIP-AUT
      • País Vasco:       Do NOT type leading zeros in CIP-AUT  
      • Comunidad Valenciana: Some models lack CIP-SNS; type leading zeros of CIP-AUT
      • Madrid:           Use CIP-SNS only (v1.4.8+)
""")


if __name__ == "__main__":
    main()
