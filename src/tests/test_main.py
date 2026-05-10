#!/usr/bin/env python3
"""
Integration tests for main application flow.
"""

import pytest
from unittest.mock import patch, MagicMock
from main import main_flow
from setup import SystemSetup
from camera import CameraCapture
from ocr_processor import OCRProcessor
from data_extractor import DataExtractor
from hid_typing import HIDTyper


class TestMainFlow:
    """Test main application flow."""

    @patch('main.cv2')
    @patch('main.time')
    def test_main_flow_integration(self, mock_time, mock_cv2):
        """Test the complete main flow."""
        # Mock time calls
        mock_time.time.side_effect = [0, 1, 2, 3]

        # Mock components
        setup = MagicMock()
        camera = MagicMock()
        camera.capture_image.return_value = "images/card.jpg"

        ocr_proc = MagicMock()
        ocr_proc.preprocess_image.return_value = MagicMock()
        ocr_proc.extract_text.return_value = "12345678AB123456 AN123456"

        data_ext = MagicMock()
        data_ext.get_primary_codes.return_value = {
            'cip_sns': '12345678AB123456',
            'cip_aut': 'AN123456'
        }

        hid_typer = MagicMock()

        # Run main flow
        main_flow(setup, camera, ocr_proc, data_ext, hid_typer)

        # Verify calls
        camera.capture_image.assert_called_once_with(setup.camera)
        ocr_proc.preprocess_image.assert_called_once_with("images/card.jpg")
        ocr_proc.extract_text.assert_called_once()
        data_ext.get_primary_codes.assert_called_once_with("12345678AB123456 AN123456")
        hid_typer.type_codes.assert_called_once_with({
            'cip_sns': '12345678AB123456',
            'cip_aut': 'AN123456'
        })
        mock_cv2.imwrite.assert_called_once()

    @patch('main.cv2')
    @patch('main.time')
    def test_main_flow_no_codes(self, mock_time, mock_cv2):
        """Test main flow when no codes found."""
        mock_time.time.side_effect = [0, 1, 2, 3]

        setup = MagicMock()
        camera = MagicMock()
        camera.capture_image.return_value = "images/card.jpg"

        ocr_proc = MagicMock()
        ocr_proc.preprocess_image.return_value = MagicMock()
        ocr_proc.extract_text.return_value = "No codes here"

        data_ext = MagicMock()
        data_ext.get_primary_codes.return_value = {
            'cip_sns': None,
            'cip_aut': None
        }

        hid_typer = MagicMock()

        main_flow(setup, camera, ocr_proc, data_ext, hid_typer)

        hid_typer.type_codes.assert_called_once_with({
            'cip_sns': None,
            'cip_aut': None
        })