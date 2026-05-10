#!/usr/bin/env python3
"""
OCR processing module for image preprocessing and text extraction.
"""

import cv2
import pytesseract
import numpy as np


class OCRProcessor:
    """Handles image preprocessing and OCR text extraction."""

    def __init__(self, roi=None, tess_config=None):
        """
        Initialize OCR processor.

        Args:
            roi: Region of interest as (x, y, w, h) in pixels, or None
            tess_config: Tesseract configuration string
        """
        self.roi = roi
        self.tess_config = tess_config or r"--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789"

    def preprocess_image(self, path):
        """
        Preprocess image for OCR.

        Args:
            path: Path to image file

        Returns:
            np.ndarray: Preprocessed image
        """
        img = cv2.imread(path)
        if img is None:
            raise ValueError(f"Cannot read image: {path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if self.roi:
            x, y, w, h = self.roi
            gray = gray[y:y+h, x:x+w]

        # Fast bilateral filter for denoising (faster than fastNlMeansDenoising)
        gray = cv2.bilateralFilter(gray, 5, 50, 50)

        # Improve OCR contrast with CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)

        # Use adaptive thresholding with tighter parameters for better text definition
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 3
        )

        # Remove small noise artifacts
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        return thresh

    def extract_text(self, img):
        """
        Extract text from preprocessed image.

        Args:
            img: Preprocessed image array

        Returns:
            str: Extracted text
        """
        return pytesseract.image_to_string(img, config=self.tess_config)