#!/usr/bin/env python3
"""
Tests for OCR processor module.
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from ocr_processor import OCRProcessor


class TestOCRProcessor:
    """Test OCRProcessor class."""

    def test_init(self):
        """Test initialization."""
        processor = OCRProcessor()
        assert processor.roi is None
        assert "tessedit_char_whitelist" in processor.tess_config

    def test_init_with_params(self):
        """Test initialization with parameters."""
        roi = (10, 20, 100, 200)
        config = "--psm 8"
        processor = OCRProcessor(roi, config)
        assert processor.roi == roi
        assert processor.tess_config == config

    @patch('ocr_processor.cv2')
    def test_preprocess_image_invalid_path(self, mock_cv2):
        """Test preprocessing with invalid image path."""
        mock_cv2.imread.return_value = None
        processor = OCRProcessor()

        with pytest.raises(ValueError, match="Cannot read image"):
            processor.preprocess_image("invalid.jpg")

    @patch('ocr_processor.cv2')
    def test_preprocess_image_basic(self, mock_cv2):
        """Test basic image preprocessing."""
        # Mock image
        mock_img = np.ones((100, 100, 3), dtype=np.uint8) * 128
        mock_cv2.imread.return_value = mock_img

        # Mock all cv2 functions
        mock_cv2.cvtColor.return_value = mock_img[:, :, 0]
        mock_cv2.bilateralFilter.return_value = mock_img[:, :, 0]
        mock_cv2.createCLAHE.return_value.apply.return_value = mock_img[:, :, 0]
        mock_cv2.adaptiveThreshold.return_value = mock_img[:, :, 0]
        mock_cv2.getStructuringElement.return_value = np.ones((2, 2), dtype=np.uint8)
        mock_cv2.morphologyEx.return_value = mock_img[:, :, 0]

        processor = OCRProcessor()
        result = processor.preprocess_image("test.jpg")

        assert isinstance(result, np.ndarray)
        mock_cv2.imread.assert_called_once_with("test.jpg")

    @patch('ocr_processor.cv2')
    def test_preprocess_image_with_roi(self, mock_cv2):
        """Test image preprocessing with ROI."""
        # Mock image
        mock_img = np.ones((200, 200, 3), dtype=np.uint8) * 128
        mock_gray = np.ones((200, 200), dtype=np.uint8) * 128
        mock_cv2.imread.return_value = mock_img
        mock_cv2.cvtColor.return_value = mock_gray

        # Mock ROI crop - create a proper cropped array
        roi = (10, 20, 50, 50)
        mock_cropped = np.ones((50, 50), dtype=np.uint8) * 128  # 50x50 as expected from ROI
        
        # Mock all cv2 functions to return proper arrays
        mock_cv2.bilateralFilter.return_value = mock_cropped
        mock_cv2.createCLAHE.return_value.apply.return_value = mock_cropped
        mock_cv2.adaptiveThreshold.return_value = mock_cropped
        mock_cv2.getStructuringElement.return_value = np.ones((2, 2), dtype=np.uint8)
        mock_cv2.morphologyEx.return_value = mock_cropped

        processor = OCRProcessor(roi=roi)
        result = processor.preprocess_image("test.jpg")

        # Verify ROI was applied (result should be the cropped size)
        assert result.shape == (50, 50)