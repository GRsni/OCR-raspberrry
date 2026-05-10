#!/usr/bin/env python3

import time
import re
import subprocess
from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import pytesseract
import numpy as np
import RPi.GPIO as GPIO

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

# Tesseract config: alphanumeric, single text line
TESS_CONFIG = r"--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789"

# Regex patterns (from your PDF)
CIP_SNS_REGEX = re.compile(r"\b\d{8}[A-Z]{2}\d{6}\b")
CIP_AUT_REGEX = re.compile(r"\b[A-Z]{2,6}\d{6,12}[A-Z]?\b|\b\d{7,12}\b")

# ----------------------------------------


def init_gpio():
    """Initialize GPIO button"""
    if not USE_BUTTON:
        return
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print(f"[INFO] GPIO button initialized on pin {BUTTON_PIN}")


def cleanup_gpio():
    """Clean up GPIO on exit"""
    if not USE_BUTTON:
        return
    GPIO.cleanup()
    print("[INFO] GPIO cleaned up")


def init_camera():
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

    
    return picam2


def capture_image(picam2):
    if DISABLE_CAMERA:
        print("[DEBUG] Camera disabled - skipping capture")
        # Create a dummy test image for button testing
        test_img = np.ones((300, 400, 3), dtype=np.uint8) * 255
        cv2.putText(test_img, "TEST MODE", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imwrite(IMAGE_ROOT_PATH + IMAGE_PATH, test_img)
        return
    
    metadata = picam2.capture_metadata()
    print("Lens position:", metadata.get("LensPosition"))

    picam2.capture_file(IMAGE_ROOT_PATH + IMAGE_PATH)


def preprocess_image(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(IMAGE_ROOT_PATH + "gray.jpg", gray)

    if ROI:
        x, y, w, h = ROI
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


def extract_text(img):
    return pytesseract.image_to_string(img, config=TESS_CONFIG)


def parse_codes(text):
    cip_sns = CIP_SNS_REGEX.findall(text)
    cip_aut = CIP_AUT_REGEX.findall(text)
    return cip_sns, cip_aut


def type_text(text):
    """
    Send text as USB keyboard input using HID gadget.
    Requires: /dev/hidg0 configured on Raspberry Pi
    """
    try:
        with open("/dev/hidg0", "rb+") as f:
            for ch in text:
                # Convert character to keyboard report
                # HID keyboard report format: [modifier, reserved, keycode1-6]
                char_lower = ch.lower()
                
                # Simple alphanumeric mapping
                keymap = {
                    '0': 0x27, '1': 0x1e, '2': 0x1f, '3': 0x20, '4': 0x21,
                    '5': 0x22, '6': 0x23, '7': 0x24, '8': 0x25, '9': 0x26,
                    'a': 0x04, 'b': 0x05, 'c': 0x06, 'd': 0x07, 'e': 0x08,
                    'f': 0x09, 'g': 0x0a, 'h': 0x0b, 'i': 0x0c, 'j': 0x0d,
                    'k': 0x0e, 'l': 0x0f, 'm': 0x10, 'n': 0x11, 'o': 0x12,
                    'p': 0x13, 'q': 0x14, 'r': 0x15, 's': 0x16, 't': 0x17,
                    'u': 0x18, 'v': 0x19, 'w': 0x1a, 'x': 0x1b, 'y': 0x1c,
                    'z': 0x1d, ' ': 0x2c, '-': 0x2d, '=': 0x2e, '[': 0x2f,
                    ']': 0x30, '\\': 0x31, ';': 0x33, "'": 0x34, '`': 0x35,
                    ',': 0x36, '.': 0x37, '/': 0x38
                }
                
                modifier = 0x02 if ch.isupper() else 0x00  # Shift for uppercase
                keycode = keymap.get(char_lower, 0x00)
                
                # Send key press
                f.write(bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00]))
                time.sleep(0.05)
                
                # Send key release
                f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
                time.sleep(0.05)
    except FileNotFoundError:
        print("[ERROR] /dev/hidg0 not found. USB HID gadget not configured.")
        print("[ERROR] Run setup-hid.sh on Raspberry Pi to enable USB HID mode.")

def main_flow(picam2=None): 
    print("[INFO] Capturing image...")
    t0 = time.time()
    capture_image(picam2)
    print(f"[INFO] Capture time: {(time.time() - t0)*1000:.1f} ms")

    print("[INFO] Preprocessing image...")
    t1 = time.time()
    img = preprocess_image(IMAGE_ROOT_PATH + IMAGE_PATH)
    print(f"[INFO] Preprocessing time: {(time.time() - t1)*1000:.1f} ms")
    cv2.imwrite(IMAGE_ROOT_PATH + "processed.jpg", img=img)

    print("[INFO] Running OCR...")
    t2 = time.time()
    text = extract_text(img)
    print(f"[INFO] OCR time: {(time.time() - t2)*1000:.1f} ms")

    print("\n--- RAW OCR OUTPUT ---")
    print(text.strip())

    cip_sns, cip_aut = parse_codes(text)

    print("\n--- PARSED RESULTS ---")
    if cip_sns:
        print("CIP-SNS:", cip_sns)
        print(f"[INFO] Typing CIP-SNS code: {cip_sns[0]}")
        type_text(cip_sns[0])
    if cip_aut:
        print("CIP-AUT:", cip_aut)
        print(f"[INFO] Typing CIP-AUT code: {cip_aut[0]}")
        type_text(cip_aut[0])
    print()


def main():
    if DISABLE_CAMERA:
        print("[DEBUG] Camera mode disabled - button testing only")
        picam2 = None
    else:
        print("[INFO] Initializing camera...")
        picam2 = init_camera()
        print("[INFO] Camera initialized. Ready to capture images.")
    
    init_gpio()
    
    if USE_BUTTON:
        print(f"[INFO] Button mode: Press GPIO pin {BUTTON_PIN} to capture")
    else:
        print("[INFO] Manual mode: Type 'c' to capture and process an image, 'q' to quit.\n")

    try:
        while True:
            if USE_BUTTON:
                # Non-blocking button check
                if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                    print("[INFO] Button pressed! Capturing image...")
                    time.sleep(0.5)  # Debounce
                    
                    main_flow()
                    
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
                   main_flow()
                else:
                    print("Invalid command. Please enter 'c' to capture or 'q' to quit.\n")
    
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
    finally:
        print("[INFO] Shutting down...")
        if picam2 is not None:
            picam2.stop()
        cleanup_gpio()


if __name__ == "__main__":
    main()
