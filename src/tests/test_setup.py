#!/usr/bin/env python3
"""
Tests for setup module.
"""

import pytest
from unittest.mock import patch, MagicMock
from setup import SystemSetup


class TestSystemSetup:
    """Test SystemSetup class."""

    def test_init(self):
        """Test initialization."""
        setup = SystemSetup()
        assert setup.camera is None
        assert setup.gpio_initialized is False

    def test_init_with_config(self):
        """Test initialization with config."""
        config = {"test": "value"}
        setup = SystemSetup(config)
        assert setup.config == config

    @patch('setup.GPIO')
    def test_init_gpio(self, mock_gpio):
        """Test GPIO initialization."""
        setup = SystemSetup()
        setup.init_gpio(button_pin=17, use_button=True)

        mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
        mock_gpio.setup.assert_called_once_with(17, mock_gpio.IN, pull_up_down=mock_gpio.PUD_UP)
        assert setup.gpio_initialized is True

    @patch('setup.GPIO')
    def test_init_gpio_disabled(self, mock_gpio):
        """Test GPIO initialization when disabled."""
        setup = SystemSetup()
        setup.init_gpio(use_button=False)

        mock_gpio.setmode.assert_not_called()
        mock_gpio.setup.assert_not_called()
        assert setup.gpio_initialized is False

    @patch('setup.GPIO')
    def test_cleanup_gpio(self, mock_gpio):
        """Test GPIO cleanup."""
        setup = SystemSetup()
        setup.gpio_initialized = True
        setup.cleanup_gpio()

        mock_gpio.cleanup.assert_called_once()
        assert setup.gpio_initialized is False

    @patch('setup.GPIO')
    def test_cleanup_gpio_not_initialized(self, mock_gpio):
        """Test GPIO cleanup when not initialized."""
        setup = SystemSetup()
        setup.cleanup_gpio()

        mock_gpio.cleanup.assert_not_called()

    @patch('setup.Picamera2')
    @patch('setup.time')
    def test_init_camera(self, mock_time, mock_picamera2):
        """Test camera initialization."""
        mock_camera = MagicMock()
        mock_picamera2.return_value = mock_camera

        setup = SystemSetup()
        result = setup.init_camera(disable_camera=False)

        mock_picamera2.assert_called_once()
        mock_camera.configure.assert_called_once()
        mock_camera.start.assert_called_once()
        mock_camera.set_controls.assert_called_once()
        assert result == mock_camera
        assert setup.camera == mock_camera

    def test_init_camera_disabled(self):
        """Test camera initialization when disabled."""
        setup = SystemSetup()
        result = setup.init_camera(disable_camera=True)

        assert result is None
        assert setup.camera is None

    @patch('builtins.open')
    def test_check_hid_device_exists(self, mock_open):
        """Test HID device check when exists."""
        mock_open.return_value.__enter__.return_value = MagicMock()
        setup = SystemSetup()
        result = setup.check_hid_device()

        assert result is True
        mock_open.assert_called_once_with("/dev/hidg0", "rb+")

    @patch('builtins.open')
    def test_check_hid_device_not_exists(self, mock_open):
        """Test HID device check when doesn't exist."""
        mock_open.side_effect = FileNotFoundError()
        setup = SystemSetup()
        result = setup.check_hid_device()

        assert result is False

    def test_setup_hid_device_exists(self):
        """Test HID setup when device exists."""
        setup = SystemSetup()
        with patch.object(setup, 'check_hid_device', return_value=True):
            result = setup.setup_hid_device()
            assert result is True

    def test_setup_hid_device_not_exists(self):
        """Test HID setup when device doesn't exist."""
        setup = SystemSetup()
        with patch.object(setup, 'check_hid_device', return_value=False):
            result = setup.setup_hid_device()
            assert result is False