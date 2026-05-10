# OCR Raspberry Pi Project

A comprehensive Optical Character Recognition (OCR) system designed for Raspberry Pi, featuring camera integration, card code extraction, and automated HID typing capabilities.

## Features

- **Camera Integration**: Real-time image capture using Raspberry Pi camera module
- **Card Code Extraction**: Detect and extract card codes from images using coordinate-based positioning
- **OCR Processing**: Leverages Tesseract OCR engine for text recognition
- **Data Extraction**: Parse and extract structured data from recognized text
- **HID Typing**: Simulate keyboard input to type extracted data automatically
- **Modular Architecture**: Well-organized codebase with separated concerns (camera, extractors, OCR processing)
- **Comprehensive Testing**: Unit tests for all major components

## Project Structure

```
src/
├── camera_module/          # Camera capture and image handling
├── extractors/             # Data extraction from images
│   ├── card_code_coordinates.py   # Card code position mapping
│   ├── card_code_extractor.py     # Extract card codes from images
│   └── data_extractor.py          # Parse extracted OCR text
├── ocr_module/             # OCR processing pipeline
│   ├── processor.py        # Main OCR processing logic
│   └── legacy.py           # Legacy OCR implementation
├── system/                 # System utilities
│   ├── hid_typing.py       # HID keyboard emulation
│   └── setup.py            # System setup and configuration
├── tests/                  # Comprehensive unit tests
├── main.py                 # Application entry point
├── quick_start.py          # Quick start example
└── ocr.py                  # Main OCR orchestration
config/
├── requirements.txt        # Python dependencies
├── setup-hid.sh           # HID setup script
└── copy.html              # Reference documentation
docs/
├── INDEX.md               # Documentation index
└── REFERENCE.md           # API reference
```

## Requirements

- Raspberry Pi (3B+ or later recommended)
- Raspberry Pi Camera Module (or compatible camera)
- Python 3.7+
- Tesseract OCR engine
- Additional dependencies listed in `config/requirements.txt`

## Installation

### 1. System Dependencies

```bash
# Install Tesseract OCR
sudo apt-get update
sudo apt-get install tesseract-ocr

# Install other system dependencies
sudo apt-get install python3-dev python3-pip
```

### 2. Camera Setup (Raspberry Pi specific)

Run the HID setup script:
```bash
bash config/setup-hid.sh
```

### 3. Python Dependencies

```bash
pip install -r config/requirements.txt
```

## Usage

### Quick Start

```python
python src/quick_start.py
```

### Run Main Application

```python
python src/main.py
```

### Using Individual Components

```python
from src.camera_module import camera
from src.ocr_module import processor
from src.extractors import card_code_extractor

# Capture image
image = camera.capture()

# Process with OCR
text_data = processor.process(image)

# Extract card codes
card_codes = card_code_extractor.extract(image, text_data)
```

## Testing

Run all tests:
```bash
./run_tests.sh
```

Or using pytest directly:
```bash
pytest -v
```

Run specific test file:
```bash
pytest src/tests/test_ocr_processor.py -v
```

## Configuration

Key configuration files:
- **`config/requirements.txt`**: Python package dependencies
- **`config/setup-hid.sh`**: HID device configuration for keyboard emulation
- **`config/copy.html`**: Reference documentation

## Key Modules

### Camera Module (`src/camera_module/`)
Handles image capture from Raspberry Pi camera or compatible devices.

### Extractors (`src/extractors/`)
- **card_code_coordinates.py**: Defines coordinate mappings for card codes
- **card_code_extractor.py**: Extracts card codes from images
- **data_extractor.py**: Parses OCR output into structured data

### OCR Module (`src/ocr_module/`)
- **processor.py**: Main OCR processing pipeline
- **legacy.py**: Legacy OCR implementation for reference

### System Module (`src/system/`)
- **hid_typing.py**: Keyboard emulation via HID interface
- **setup.py**: System configuration and initialization

## Documentation

See [docs/INDEX.md](docs/INDEX.md) for full documentation and [docs/REFERENCE.md](docs/REFERENCE.md) for API reference.

## Development Notes

- Ensure camera is properly connected and enabled on Raspberry Pi
- HID device must be properly configured for keyboard emulation to work
- Test individual components before integrating the full pipeline
- Update coordinates in `card_code_coordinates.py` based on your specific use case

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues, questions, or contributions, please refer to the project documentation or contact the maintainers.
