#!/usr/bin/env python3
"""
Main OCR application refactored into modules.
"""

import time
import cv2
from setup import SystemSetup
from camera import CameraCapture
from ocr_processor import OCRProcessor
from data_extractor import DataExtractor
from hid_typing import HIDTyper


# ---------------- CONFIG ----------------

IMAGE_ROOT_PATH = "images/"
IMAGE_PATH = "card.jpg"
ROI = None
PRINT_DEBUG = True
BUTTON_PIN = 17  # GPIO pin for capture button (physical pin 11)
USE_BUTTON = True  # Set to False to disable GPIO button
DISABLE_CAMERA = False  # Set to True to disable camera and test button only

# Example ROI if you want to hard-crop (x, y, w, h)
# ROI = (400, 900, 2200, 400)

# ----------------------------------------


def main_flow(setup, camera, ocr_proc, data_ext, hid_typer):
    """Execute the main OCR flow."""
    print("[INFO] Capturing image...")
    t0 = time.time()
    image_path = camera.capture_image(setup.camera)
    print(".1f")

    print("[INFO] Preprocessing image...")
    t1 = time.time()
    img = ocr_proc.preprocess_image(image_path)
    print(".1f")
    cv2.imwrite(IMAGE_ROOT_PATH + "processed.jpg", img)

    print("[INFO] Running OCR...")
    t2 = time.time()
    text = ocr_proc.extract_text(img)
    print(".1f")

    print("\n--- RAW OCR OUTPUT ---")
    print(text.strip())

    codes = data_ext.get_primary_codes(text)

    print("\n--- PARSED RESULTS ---")
    if codes['cip_sns']:
        print("CIP-SNS:", codes['cip_sns'])
    if codes['cip_aut']:
        print("CIP-AUT:", codes['cip_aut'])

    hid_typer.type_codes(codes)
    print()


def main():
    """Main application entry point."""
    # Initialize components
    setup = SystemSetup()
    camera = CameraCapture(IMAGE_ROOT_PATH, IMAGE_PATH, DISABLE_CAMERA)
    ocr_proc = OCRProcessor(ROI)
    data_ext = DataExtractor()
    hid_typer = HIDTyper()

    if DISABLE_CAMERA:
        print("[DEBUG] Camera mode disabled - button testing only")
        picam2 = None
    else:
        print("[INFO] Initializing camera...")
        picam2 = setup.init_camera(DISABLE_CAMERA)
        print("[INFO] Camera initialized. Ready to capture images.")

    setup.init_gpio(BUTTON_PIN, USE_BUTTON)

    if USE_BUTTON:
        print(f"[INFO] Button mode: Press GPIO pin {BUTTON_PIN} to capture")
    else:
        print("[INFO] Manual mode: Type 'c' to capture and process an image, 'q' to quit.\n")

    try:
        while True:
            if USE_BUTTON:
                # Non-blocking button check
                if setup.gpio_initialized:
                    import RPi.GPIO as GPIO
                    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                        print("[INFO] Button pressed! Capturing image...")
                        time.sleep(0.5)  # Debounce
                    
                        main_flow(setup, camera, ocr_proc, data_ext, hid_typer)
                    
                        # Wait for button release
                        while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                            time.sleep(0.1)
                        time.sleep(0.5)  # Debounce release
                
                time.sleep(0.1)  # Check button every 100ms
            else:
                # Manual mode
                user_input = input("Enter command (c=capture, q=quit): ").strip().lower()

                if user_input == 'q':
                    print("[INFO] Shutting down...")
                    break
                elif user_input == 'c':
                   main_flow(setup, camera, ocr_proc, data_ext, hid_typer)
                else:
                    print("Invalid command. Please enter 'c' to capture or 'q' to quit.\n")

    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
    finally:
        print("[INFO] Shutting down...")
        if picam2 is not None:
            picam2.stop()
        setup.cleanup_gpio()


if __name__ == "__main__":
    main()