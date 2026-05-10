#!/usr/bin/env python3
"""
Data extraction module for parsing CIP codes from OCR text.
"""

import re


class DataExtractor:
    """Extracts and parses CIP-SNS and CIP-AUT codes from text."""

    def __init__(self):
        """Initialize with regex patterns."""
        # Regex patterns (from your PDF)
        self.cip_sns_regex = re.compile(r"\b\d{8}[A-Z]{2}\d{6}\b")
        self.cip_aut_regex = re.compile(r"\b[A-Z]{2,6}\d{6,12}[A-Z]?\b|\b\d{7,12}\b")

    def parse_codes(self, text):
        """
        Parse CIP-SNS and CIP-AUT codes from text.

        Args:
            text: Raw OCR text

        Returns:
            tuple: (cip_sns_list, cip_aut_list)
        """
        cip_sns = self.cip_sns_regex.findall(text)
        cip_aut = self.cip_aut_regex.findall(text)
        return cip_sns, cip_aut

    def get_primary_codes(self, text):
        """
        Get the primary codes to use (first match of each type).

        Args:
            text: Raw OCR text

        Returns:
            dict: {'cip_sns': str or None, 'cip_aut': str or None}
        """
        cip_sns, cip_aut = self.parse_codes(text)
        return {
            'cip_sns': cip_sns[0] if cip_sns else None,
            'cip_aut': cip_aut[0] if cip_aut else None
        }