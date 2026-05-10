#!/usr/bin/env python3
"""
Tests for camera module.
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from camera import CameraCapture


class TestCameraCapture:
    """Test CameraCapture class."""

    def test_init(self):
        """Test initialization."""
        camera = CameraCapture()
        assert camera.image_root_path == "images/"
        assert camera.image_path == "card.jpg"
        assert camera.disable_camera is False

    def test_init_custom_params(self):
        """Test initialization with custom parameters."""
        camera = CameraCapture("custom/", "test.jpg", True)
        assert camera.image_root_path == "custom/"
        assert camera.image_path == "test.jpg"
        assert camera.disable_camera is True

    @patch('camera.cv2')
    def test_capture_image_disabled(self, mock_cv2):
        """Test image capture when camera disabled."""
        camera = CameraCapture(disable_camera=True)
        result = camera.capture_image(None)

        expected_path = "images/card.jpg"
        assert result == expected_path
        mock_cv2.imwrite.assert_called_once()

    def test_capture_image_no_camera(self):
        """Test image capture with no camera."""
        camera = CameraCapture(disable_camera=False)
        with pytest.raises(ValueError, match="Camera not initialized"):
            camera.capture_image(None)

    @patch('camera.cv2')
    def test_capture_image_with_camera(self, mock_cv2):
        """Test image capture with camera."""
        mock_camera = MagicMock()
        mock_camera.capture_metadata.return_value = {"LensPosition": 10.0}

        camera = CameraCapture()
        result = camera.capture_image(mock_camera)

        expected_path = "images/card.jpg"
        assert result == expected_path
        mock_camera.capture_metadata.assert_called_once()
        mock_camera.capture_file.assert_called_once_with(expected_path)