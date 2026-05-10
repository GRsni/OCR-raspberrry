#!/usr/bin/env python3
"""
Camera module for image capture operations.
"""

import cv2
import numpy as np


class CameraCapture:
    """Handles camera operations and image capture."""

    def __init__(self, image_root_path="images/", image_path="card.jpg", disable_camera=False):
        """
        Initialize camera capture.

        Args:
            image_root_path: Directory to save images
            image_path: Filename for captured image
            disable_camera: If True, create dummy images
        """
        self.image_root_path = image_root_path
        self.image_path = image_path
        self.disable_camera = disable_camera

    def capture_image(self, picam2):
        """
        Capture image using camera or create dummy image.

        Args:
            picam2: Picamera2 instance

        Returns:
            str: Path to captured image
        """
        full_path = self.image_root_path + self.image_path

        if self.disable_camera:
            print("[DEBUG] Camera disabled - creating test image")
            # Create a dummy test image for button testing
            test_img = np.ones((300, 400, 3), dtype=np.uint8) * 255
            cv2.putText(test_img, "TEST MODE", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.imwrite(full_path, test_img)
            return full_path

        if picam2 is None:
            raise ValueError("Camera not initialized")

        metadata = picam2.capture_metadata()
        print("Lens position:", metadata.get("LensPosition"))

        picam2.capture_file(full_path)
        return full_path