#!/usr/bin/env python3
"""
HID typing module for sending text via USB HID gadget.
"""

import time


class HIDTyper:
    """Handles typing text via USB HID device."""

    def __init__(self, device_path="/dev/hidg0"):
        """
        Initialize HID typer.

        Args:
            device_path: Path to HID device
        """
        self.device_path = device_path
        self.keymap = {
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

    def type_text(self, text):
        """
        Send text as USB keyboard input.

        Args:
            text: Text to type
        """
        try:
            with open(self.device_path, "rb+") as f:
                for ch in text:
                    char_lower = ch.lower()

                    # Simple alphanumeric mapping
                    modifier = 0x02 if ch.isupper() else 0x00  # Shift for uppercase
                    keycode = self.keymap.get(char_lower, 0x00)

                    # Send key press
                    f.write(bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00]))
                    time.sleep(0.05)

                    # Send key release
                    f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
                    time.sleep(0.05)
        except FileNotFoundError:
            print(f"[ERROR] {self.device_path} not found. USB HID gadget not configured.")
            raise

    def type_codes(self, codes):
        """
        Type CIP codes.

        Args:
            codes: Dict with 'cip_sns' and 'cip_aut' keys
        """
        if codes.get('cip_sns'):
            print(f"[INFO] Typing CIP-SNS code: {codes['cip_sns']}")
            self.type_text(codes['cip_sns'])

        if codes.get('cip_aut'):
            print(f"[INFO] Typing CIP-AUT code: {codes['cip_aut']}")
            self.type_text(codes['cip_aut'])