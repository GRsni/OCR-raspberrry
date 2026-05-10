#!/usr/bin/env python3
"""
Comprehensive tests for OCR system components.
"""

import pytest

from setup import SystemSetup
from camera import CameraCapture
from ocr_processor import OCRProcessor
from data_extractor import DataExtractor
from hid_typing import HIDTyper


def test_system_setup():
    """Test basic system setup."""
    setup = SystemSetup()
    assert setup.camera is None
    assert not setup.gpio_initialized
    print("✓ System setup test passed")


def test_camera_capture():
    """Test camera capture initialization."""
    camera = CameraCapture()
    assert camera.image_root_path == "images/"
    assert camera.image_path == "card.jpg"
    print("✓ Camera capture test passed")


def test_ocr_processor():
    """Test OCR processor initialization."""
    processor = OCRProcessor()
    assert processor.roi is None
    assert "tessedit" in processor.tess_config
    print("✓ OCR processor test passed")


def test_data_extractor():
    """Test data extractor functionality."""
    extractor = DataExtractor()

    # Test with sample text
    text = "CIP-SNS: 12345678AB123456 and CIP-AUT: AN123456789"
    codes = extractor.get_primary_codes(text)

    assert codes['cip_sns'] == '12345678AB123456'
    assert codes['cip_aut'] == 'AN123456789'
    print("✓ Data extractor test passed")


def test_hid_typer():
    """Test HID typer initialization."""
    typer = HIDTyper()
    assert typer.device_path == "/dev/hidg0"
    assert 'a' in typer.keymap
    assert '0' in typer.keymap
    print("✓ HID typer test passed")


def test_integration_flow():
    """Test basic integration flow."""
    # This would be a more comprehensive integration test
    # For now, just verify all components can be instantiated
    setup = SystemSetup()
    camera = CameraCapture(disable_camera=True)  # Disable for testing
    ocr_proc = OCRProcessor()
    data_ext = DataExtractor()
    hid_typer = HIDTyper()

    # Verify all objects created successfully
    assert setup is not None
    assert camera is not None
    assert ocr_proc is not None
    assert data_ext is not None
    assert hid_typer is not None
    print("✓ Integration flow test passed")


if __name__ == "__main__":
    print("Running comprehensive OCR system tests...")
    print("=" * 50)

    try:
        test_system_setup()
        test_camera_capture()
        test_ocr_processor()
        test_data_extractor()
        test_hid_typer()
        test_integration_flow()

        print("=" * 50)
        print("✓ All tests passed!")

    except Exception as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)

