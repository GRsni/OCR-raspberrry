#!/usr/bin/env python3
"""
Setup module for OCR system initialization.

Handles GPIO setup, camera initialization, and HID device configuration.
"""

import time
import subprocess
from picamera2 import Picamera2, Preview
from libcamera import controls
import RPi.GPIO as GPIO


class SystemSetup:
    """Handles system setup for OCR operations."""

    def __init__(self, config=None):
        """
        Initialize system setup.

        Args:
            config: Configuration dictionary with setup parameters
        """
        self.config = config or {}
        self.camera = None
        self.gpio_initialized = False

    def init_gpio(self, button_pin=17, use_button=True):
        """
        Initialize GPIO for button input.

        Args:
            button_pin: GPIO pin number for capture button
            use_button: Whether to use GPIO button
        """
        if not use_button:
            return

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio_initialized = True
        print(f"[INFO] GPIO button initialized on pin {button_pin}")

    def cleanup_gpio(self):
        """Clean up GPIO resources."""
        if self.gpio_initialized:
            GPIO.cleanup()
            self.gpio_initialized = False
            print("[INFO] GPIO cleaned up")

    def init_camera(self, disable_camera=False):
        """
        Initialize camera for image capture.

        Args:
            disable_camera: If True, skip camera initialization
        """
        if disable_camera:
            print("[DEBUG] Camera disabled")
            return None

        picam2 = Picamera2()

        config = picam2.create_still_configuration(
            main={"size": (300, 100)},
            controls={
                "FrameRate": 10
            }
        )

        picam2.configure(config)
        picam2.start()

        # Give sensor time to power up
        time.sleep(0.5)

        # Set focus to closest possible distance (manual focus mode)
        picam2.set_controls({
            "AfMode": controls.AfModeEnum.Manual,
            "LensPosition": 10.0  # Closest focus distance
        })

        print("[INFO] Focus set to closest distance")
        self.camera = picam2
        return picam2

    def check_hid_device(self):
        """
        Check if HID gadget device is available.

        Returns:
            bool: True if /dev/hidg0 exists
        """
        try:
            with open("/dev/hidg0", "rb+") as f:
                return True
        except FileNotFoundError:
            return False

    def setup_hid_device(self):
        """
        Setup HID device if not available.
        Requires setup-hid.sh script to be run as root.
        """
        if not self.check_hid_device():
            print("[ERROR] /dev/hidg0 not found. USB HID gadget not configured.")
            print("[ERROR] Run setup-hid.sh on Raspberry Pi to enable USB HID mode.")
            return False
        return True