"""
Card Code Coordinates for Spanish Health Insurance Cards (Tarjetas Sanitarias SNS)

This module defines the expected locations of CIP_SNS and CIP_AUT codes
on health insurance cards for each Spanish autonomous community.

Based on: "Modelos de Tarjetas Sanitarias en el SNS - V1.4.8"

Coordinate System:
- Normalized to card filling 100% of the image frame
- Values are percentages (0-100) of image width (W) and height (H)
- Origin (0,0) is top-left; (100,100) is bottom-right
- Each location includes:
  * x_min, x_max, y_min, y_max: Bounding box percentages
  * ocr_pattern: Regex pattern to match the code
  * color_hint: Expected color range for visual validation
  * notes: Special considerations or variants
"""

CARD_COORDINATES = {
    "Andalucía": {
        "structure": "AN + 10 or 12 numbers",
        "variants": [
            {
                "name": "Modelo único (RD 702/2013) - newer",
                "cip_sns": {
                    "x_min": 35,
                    "x_max": 70,
                    "y_min": 65,
                    "y_max": 78,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "CIP-SNS: 8 chars (2 letters + 6 numbers)"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 35,
                    "y_min": 48,
                    "y_max": 58,
                    "ocr_pattern": r"AN[0-9]{10,12}",
                    "color_hint": "black_text_on_white",
                    "notes": "CIP-AUT: AN + 10 or 12 numbers (red box in doc)"
                }
            },
            {
                "name": "Older models with NAF identifier",
                "cip_sns": {
                    "x_min": 35,
                    "x_max": 70,
                    "y_min": 65,
                    "y_max": 78,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "CIP-SNS might not be present in older cards"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 35,
                    "y_min": 30,
                    "y_max": 45,
                    "ocr_pattern": r"(NAF|AN)[0-9]{8,12}",
                    "color_hint": "black_text_on_white",
                    "notes": "NAF code used as patient identifier in older models"
                }
            }
        ]
    },

    "Aragón": {
        "structure": "AR + 9 numbers + 1 letter",
        "variants": [
            {
                "name": "Formato único (RD 702/2013)",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"AR[0-9]{9}[A-Z]",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box in document"
                }
            }
        ]
    },

    "Asturias": {
        "structure": "ASTU + 12 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013)",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"ASTU[0-9]{12}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box in document"
                }
            }
        ]
    },

    "Baleares": {
        "structure": "11 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013) - V1.4.5 2018",
                "cip_sns": {
                    "x_min": 35,
                    "x_max": 70,
                    "y_min": 68,
                    "y_max": 80,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 48,
                    "y_max": 62,
                    "ocr_pattern": r"[0-9]{11}",
                    "color_hint": "black_text_on_white",
                    "notes": "11 numbers only (red box)"
                }
            }
        ]
    },

    "Canarias": {
        "structure": "4 letters + 12 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013) - V1.4.4 2018",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[A-Z]{4}[0-9]{12}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box in document"
                }
            }
        ]
    },

    "Cantabria": {
        "structure": "4 letters + 12 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013)",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[A-Z]{4}[0-9]{12}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box in document"
                }
            }
        ]
    },

    "Castilla La Mancha": {
        "structure": "4 letters + 12 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013) - V1.4.3 2017",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[A-Z]{4}[0-9]{12}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box in document"
                }
            }
        ]
    },

    "Castilla y León": {
        "structure": "4 letters + 12 numbers OR CYL + 10 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013) - newer",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"([A-Z]{4}[0-9]{12}|CYL[0-9]{10})",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box in document - may be 4 letters + 12 or CYL + 10"
                }
            }
        ]
    },

    "Cataluña": {
        "structure": "4 letters + 10 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013)",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[A-Z]{4}[0-9]{10}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box in document. CITE on back (barcode)."
                }
            }
        ]
    },

    "Comunidad Valenciana": {
        "structure": "7-8 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013) - V1.4.1 unified",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document. NO CIP-SNS in some models."
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[0-9]{7,8}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box. 7-8 numbers. Type leading zeros when data entry needed."
                }
            }
        ]
    },

    "Extremadura": {
        "structure": "4 letters + 12 numbers OR CAEX + 12 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013) - newer",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"([A-Z]{4}[0-9]{12}|CAEX[0-9]{12})",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box in document - may be 4 letters + 12 or CAEX + 12"
                }
            }
        ]
    },

    "Galicia": {
        "structure": "6 numbers + 4 letters + 4 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013)",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[0-9]{6}[A-Z]{4}[0-9]{4}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box: 6 numbers + 4 letters + 4 numbers"
                }
            }
        ]
    },

    "La Rioja": {
        "structure": "4 letters + 12 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013) - V1.4.6 2019",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[A-Z]{4}[0-9]{12}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box in document"
                }
            }
        ]
    },

    "Madrid": {
        "structure": "4 letters + 12 numbers OR 10 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013) - V1.4.8 2019 with CIP-SNS keypad",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box. Data entry REQUIRES CIP-SNS typing (not CIP-AUT)."
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"([A-Z]{4}[0-9]{12}|[0-9]{10})",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box. 4 letters + 12 numbers OR 10 numbers (newer models)"
                }
            }
        ]
    },

    "Murcia": {
        "structure": "4 letters + 12 numbers OR CARM + 12 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013)",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"([A-Z]{4}[0-9]{12}|CARM[0-9]{12})",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box - may be 4 letters + 12 or CARM + 12"
                }
            }
        ]
    },

    "Navarra": {
        "structure": "8 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013) - V1.4.2 clarification",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box. Si TECLEAR LOS CEROS (type leading zeros)."
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[0-9]{8}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box: 8 numbers. MUST type leading zeros if present."
                }
            }
        ]
    },

    "País Vasco": {
        "structure": "8 numbers",
        "variants": [
            {
                "name": "Formato único (RD 702/2013) - V1.4.2 clarification",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box. NO TECLEAR LOS CEROS (don't type leading zeros)."
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[0-9]{8}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box: 8 numbers. DO NOT type leading zeros during data entry."
                }
            }
        ]
    },

    "Ceuta": {
        "structure": "4 letters + 12 numbers",
        "variants": [
            {
                "name": "INGESA - Formato único (RD 702/2013)",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[A-Z]{4}[0-9]{12}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box. INGESA (Instituto Nacional de Gestión Sanitaria)"
                }
            }
        ]
    },

    "Melilla": {
        "structure": "4 letters + 12 numbers",
        "variants": [
            {
                "name": "INGESA - Formato único (RD 702/2013)",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[A-Z]{4}[0-9]{12}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box. INGESA (Instituto Nacional de Gestión Sanitaria)"
                }
            }
        ]
    },

    "INGESA": {
        "structure": "4 letters + 12 numbers",
        "variants": [
            {
                "name": "Instituto Nacional de Gestión Sanitaria - Formato único (RD 702/2013)",
                "cip_sns": {
                    "x_min": 40,
                    "x_max": 75,
                    "y_min": 70,
                    "y_max": 82,
                    "ocr_pattern": r"[A-Z]{1}[A-Z]{1}[0-9]{6}",
                    "color_hint": "black_text_on_white",
                    "notes": "Green box in document"
                },
                "cip_aut": {
                    "x_min": 5,
                    "x_max": 40,
                    "y_min": 45,
                    "y_max": 60,
                    "ocr_pattern": r"[A-Z]{4}[0-9]{12}",
                    "color_hint": "black_text_on_white",
                    "notes": "Red box. Covers Ceuta, Melilla, and INGESA institutions (V1.4.7 2019)"
                }
            }
        ]
    }
}

# Additional reference info
GENERAL_RULES = {
    "cip_sns": {
        "format": "2 letters + 6 numbers",
        "length": 8,
        "assigned_by": "Ministerio de Sanidad",
        "description": "Código de Identificación Personal único del Sistema Nacional de Salud",
        "priority": "PRIMARY - Use this code first when possible",
        "location_y_range": "bottom third of card (65-85% from top)",
    },
    "cip_aut": {
        "format": "Variable by community (see structure field)",
        "assigned_by": "Each autonomous community administration",
        "description": "Código autonómico de identificación del paciente",
        "priority": "SECONDARY - Use only if CIP-SNS not available",
        "location_y_range": "middle section of card (40-65% from top)",
    },
    "cite": {
        "description": "Identificador de la comunidad autónoma emisora",
        "notes": "Reference only; typically found near other codes",
    }
}

SPECIAL_NOTES = {
    "Navarra": "SI TECLEAR LOS CEROS INCLUIDOS AL PRINCIPIO DEL CIP-AUT (Type leading zeros)",
    "País Vasco": "NO TECLEAR LOS CEROS INCLUIDOS AL PRINCIPIO DEL CIP-AUT (Do NOT type leading zeros)",
    "Comunidad Valenciana": "NO CIP-SNS in some models - Type leading zeros of CIP-AUT",
    "Madrid": "V1.4.8: Data entry REQUIRES typing CIP-SNS (not CIP-AUT)",
    "Cataluña": "CITE appears in barcode on reverse side",
}

if __name__ == "__main__":
    import json
    
    # Print summary
    print("=" * 80)
    print("SPANISH HEALTH INSURANCE CARD (SNS) CODE LOCATION REFERENCE")
    print("=" * 80)
    print(f"\nTotal Communities/Institutions: {len(CARD_COORDINATES)}")
    print("\nCommunities defined:")
    for i, community in enumerate(CARD_COORDINATES.keys(), 1):
        variants = len(CARD_COORDINATES[community]['variants'])
        print(f"  {i:2}. {community:30} ({variants} variant{'s' if variants > 1 else ''})")
    
    print("\n" + "=" * 80)
    print("GENERAL RULES")
    print("=" * 80)
    print(f"CIP-SNS: {GENERAL_RULES['cip_sns']['description']}")
    print(f"  Format: {GENERAL_RULES['cip_sns']['format']}")
    print(f"  Priority: {GENERAL_RULES['cip_sns']['priority']}")
    print(f"\nCIP-AUT: {GENERAL_RULES['cip_aut']['description']}")
    print(f"  Format: Variable by community")
    print(f"  Priority: {GENERAL_RULES['cip_aut']['priority']}")
    
    print("\n" + "=" * 80)
    print("COORDINATE SYSTEM")
    print("=" * 80)
    print("- Card fills 100% of the image frame")
    print("- Normalized coordinates: 0-100 (percentage of image width/height)")
    print("- Origin (0,0): top-left")
    print("- Point (100,100): bottom-right")
    print("- x_min, x_max, y_min, y_max define bounding boxes")
