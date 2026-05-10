# Spanish Health Insurance Card Code Locations Reference

## Overview

This document defines the precise locations of **CIP-SNS** and **CIP-AUT** codes on Spanish health insurance cards (Tarjetas Sanitarias SNS) across all autonomous communities.

### Key Definitions

- **CIP-SNS**: Código de Identificación Personal (Unique National Health System identifier)
  - Format: 2 letters + 6 numbers (8 chars total)
  - Assigned by: Ministry of Health (Ministerio de Sanidad)
  - **Priority: PRIMARY** - Use this code first when possible
  - Location: Bottom third of card (typically 65-85% from top)

- **CIP-AUT**: Autonomous Community Identification Code
  - Format: Variable by community (see detailed list below)
  - Assigned by: Each autonomous community administration
  - **Priority: SECONDARY** - Use only if CIP-SNS unavailable
  - Location: Middle section of card (typically 40-65% from top)

- **CITE**: Identifier of the issuing autonomous community (reference only)

---

## Coordinate System

All coordinates are **normalized to 100% card coverage** (card fills entire image frame):
- **X-axis**: 0-100 = left edge to right edge
- **Y-axis**: 0-100 = top edge to bottom edge
- **Origin**: (0,0) = top-left corner
- **Max point**: (100,100) = bottom-right corner

Each code location includes:
- **x_min, x_max, y_min, y_max**: Bounding box percentages
- **ocr_pattern**: Regex pattern to validate extracted text
- **color_hint**: Expected text color
- **notes**: Special instructions or variants

---

## All Communities & Coordinate Locations

### 1. **Andalucía**
**Structure**: AN + 10 or 12 numbers

#### Variant A: Formato único (RD 702/2013) - newer models
- **CIP-SNS**:
  - Box: (35-70% W, 65-78% H)
  - Pattern: `[A-Z]{1}[A-Z]{1}[0-9]{6}`
  - Format: 2 letters + 6 numbers
  
- **CIP-AUT**:
  - Box: (5-35% W, 48-58% H)
  - Pattern: `AN[0-9]{10,12}`
  - Format: AN + 10 or 12 numbers

#### Variant B: Older models with NAF identifier
- **CIP-AUT**:
  - Box: (5-35% W, 30-45% H)
  - Pattern: `(NAF|AN)[0-9]{8,12}`
  - Note: NAF used as patient identifier in legacy models

---

### 2. **Aragón**
**Structure**: AR + 9 numbers + 1 letter
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `AR[0-9]{9}[A-Z]`

---

### 3. **Asturias**
**Structure**: ASTU + 12 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `ASTU[0-9]{12}`

---

### 4. **Baleares (Illes)**
**Structure**: 11 numbers (v1.4.5, 2018)
- **CIP-SNS**: (35-70% W, 68-80% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 48-62% H) — `[0-9]{11}`

---

### 5. **Canarias**
**Structure**: 4 letters + 12 numbers (v1.4.4, 2018)
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[A-Z]{4}[0-9]{12}`

---

### 6. **Cantabria**
**Structure**: 4 letters + 12 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[A-Z]{4}[0-9]{12}`

---

### 7. **Castilla La Mancha**
**Structure**: 4 letters + 12 numbers (v1.4.3, 2017)
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[A-Z]{4}[0-9]{12}`

---

### 8. **Castilla y León**
**Structure**: 4 letters + 12 numbers OR CYL + 10 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `([A-Z]{4}[0-9]{12}|CYL[0-9]{10})`

---

### 9. **Cataluña**
**Structure**: 4 letters + 10 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[A-Z]{4}[0-9]{10}`
- **Note**: CITE appears in barcode on reverse side

---

### 10. **Comunidad Valenciana**
**Structure**: 7-8 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
  - **⚠️ WARNING**: Some models do NOT have CIP-SNS printed
- **CIP-AUT**: (5-40% W, 45-60% H) — `[0-9]{7,8}`
- **Special**: **MUST type leading zeros** when entering CIP-AUT in data system

---

### 11. **Extremadura**
**Structure**: 4 letters + 12 numbers OR CAEX + 12 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `([A-Z]{4}[0-9]{12}|CAEX[0-9]{12})`

---

### 12. **Galicia**
**Structure**: 6 numbers + 4 letters + 4 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[0-9]{6}[A-Z]{4}[0-9]{4}`

---

### 13. **La Rioja**
**Structure**: 4 letters + 12 numbers (v1.4.6, 2019)
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[A-Z]{4}[0-9]{12}`

---

### 14. **Madrid**
**Structure**: 4 letters + 12 numbers OR 10 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `([A-Z]{4}[0-9]{12}|[0-9]{10})`
- **Special (v1.4.8, 2019)**: Data entry **REQUIRES typing CIP-SNS** (not CIP-AUT)
  - Newer 10-number variant available in some models

---

### 15. **Murcia (Región de)**
**Structure**: 4 letters + 12 numbers OR CARM + 12 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `([A-Z]{4}[0-9]{12}|CARM[0-9]{12})`

---

### 16. **Navarra (Comunidad Foral de)**
**Structure**: 8 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[0-9]{8}`
- **Special (v1.4.2)**: **SÍ TECLEAR LOS CEROS** (Yes, type leading zeros)
  - If CIP-AUT is "00123456", type exactly as shown with leading zeros

---

### 17. **País Vasco (Euskadi)**
**Structure**: 8 numbers
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[0-9]{8}`
- **Special (v1.4.2)**: **NO TECLEAR LOS CEROS** (Don't type leading zeros)
  - If CIP-AUT is "00123456", type only "123456" (remove leading zeros)

---

### 18. **Ceuta**
**Structure**: 4 letters + 12 numbers (INGESA, v1.4.7, 2019)
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[A-Z]{4}[0-9]{12}`
- **Note**: Instituto Nacional de Gestión Sanitaria (INGESA)

---

### 19. **Melilla**
**Structure**: 4 letters + 12 numbers (INGESA, v1.4.7, 2019)
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[A-Z]{4}[0-9]{12}`
- **Note**: Instituto Nacional de Gestión Sanitaria (INGESA)

---

### 20. **INGESA** (Instituto Nacional de Gestión Sanitaria)
**Structure**: 4 letters + 12 numbers (v1.4.7, 2019)
- **CIP-SNS**: (40-75% W, 70-82% H) — `[A-Z]{1}[A-Z]{1}[0-9]{6}`
- **CIP-AUT**: (5-40% W, 45-60% H) — `[A-Z]{4}[0-9]{12}`
- **Note**: Covers Ceuta, Melilla, and INGESA institutions

---

## Important Special Cases

### Data Entry Rules

| Community | Leading Zeros | Notes |
|-----------|---|---|
| **Navarra** | **YES** type them | Type CIP-AUT exactly as printed with all leading zeros |
| **País Vasco** | **NO** don't type | Remove all leading zeros from CIP-AUT |
| **Comunidad Valenciana** | **YES** type them | Type CIP-AUT with leading zeros included |
| **Madrid** | N/A | Use **CIP-SNS** only (mandatory in v1.4.8+) |

### Missing Codes

- **Comunidad Valenciana**: Some card models **do NOT have CIP-SNS** printed on front
  - In these cases, CIP-AUT must be used as fallback
  - Remember to type leading zeros

### Identifier Variants

- **Andalucía**: Older cards use **NAF** code instead of standard CIP-AUT
  - Location: (5-35% W, 30-45% H) for NAF variants
  
- **Cataluña**: **CITE code on reverse** in barcode (not visible on front face)

---

## Usage in Code

### Python Example

```python
from card_code_extractor import CardCodeExtractor, display_coordinates

# Display coordinates for reference
display_coordinates('Andalucía')

# Extract codes from an image
extractor = CardCodeExtractor('card_photo.jpg')
result = extractor.find_codes_in_community('Andalucía', variant_idx=0)

print(f"CIP-SNS: {result['cip_sns']} (confidence: {result['cip_sns_confidence']})")
print(f"CIP-AUT: {result['cip_aut']} (confidence: {result['cip_aut_confidence']})")

# For Navarra: remember to type leading zeros
if result['community'] == 'Navarra':
    print("⚠️ Reminder: Type CIP-AUT with leading zeros")
```

---

## Document Reference

**Source**: Modelos de Tarjetas Sanitarias en el SNS - V1.4.8 (15/03/2019)

**Legal Basis**: Real Decreto 702/2013 (RD 702/2013)

**Last Updated**: 15/03/2019 (v1.4.8)

---

## Files Included

1. **card_code_coordinates.py** — Complete coordinate definitions for all 20 communities
2. **card_code_extractor.py** — Utility class for extracting codes from images
3. **REFERENCE.md** — This file (quick reference guide)

