#!/usr/bin/env python3
"""
Tests for data extractor module.
"""

import pytest
from data_extractor import DataExtractor


class TestDataExtractor:
    """Test DataExtractor class."""

    def test_init(self):
        """Test initialization."""
        extractor = DataExtractor()
        assert extractor.cip_sns_regex is not None
        assert extractor.cip_aut_regex is not None

    def test_parse_codes_no_codes(self):
        """Test parsing text with no codes."""
        extractor = DataExtractor()
        text = "This is just some random text with no codes."
        cip_sns, cip_aut = extractor.parse_codes(text)

        assert cip_sns == []
        assert cip_aut == []

    def test_parse_codes_cip_sns(self):
        """Test parsing CIP-SNS codes."""
        extractor = DataExtractor()
        text = "Some text 12345678AB123456 more text"
        cip_sns, cip_aut = extractor.parse_codes(text)

        assert len(cip_sns) == 1
        assert cip_sns[0] == "12345678AB123456"
        assert cip_aut == []

    def test_parse_codes_cip_aut(self):
        """Test parsing CIP-AUT codes."""
        extractor = DataExtractor()
        text = "Code: AN123456789012 and some other text"
        cip_sns, cip_aut = extractor.parse_codes(text)

        assert cip_sns == []
        assert len(cip_aut) == 1
        assert cip_aut[0] == "AN123456789012"

    def test_parse_codes_both(self):
        """Test parsing both CIP-SNS and CIP-AUT codes."""
        extractor = DataExtractor()
        text = "CIP-SNS: 12345678AB123456 and CIP-AUT: AR123456789"
        cip_sns, cip_aut = extractor.parse_codes(text)

        assert len(cip_sns) == 1
        assert cip_sns[0] == "12345678AB123456"
        assert len(cip_aut) == 1
        assert cip_aut[0] == "AR123456789"

    def test_parse_codes_multiple(self):
        """Test parsing multiple codes."""
        extractor = DataExtractor()
        text = "First: 12345678AB123456 Second: 87654321CD654321 Third: AN123456"
        cip_sns, cip_aut = extractor.parse_codes(text)

        assert len(cip_sns) == 2
        assert cip_sns == ["12345678AB123456", "87654321CD654321"]
        assert len(cip_aut) == 1
        assert cip_aut[0] == "AN123456"

    def test_get_primary_codes_none(self):
        """Test getting primary codes when none found."""
        extractor = DataExtractor()
        text = "No codes here"
        result = extractor.get_primary_codes(text)

        assert result == {'cip_sns': None, 'cip_aut': None}

    def test_get_primary_codes_both(self):
        """Test getting primary codes."""
        extractor = DataExtractor()
        text = "CIP-SNS: 12345678AB123456 and CIP-AUT: AR123456789"
        result = extractor.get_primary_codes(text)

        assert result == {
            'cip_sns': '12345678AB123456',
            'cip_aut': 'AR123456789'
        }

    def test_get_primary_codes_only_sns(self):
        """Test getting primary codes with only CIP-SNS."""
        extractor = DataExtractor()
        text = "Only CIP-SNS: 12345678AB123456"
        result = extractor.get_primary_codes(text)

        assert result == {
            'cip_sns': '12345678AB123456',
            'cip_aut': None
        }

    def test_get_primary_codes_only_aut(self):
        """Test getting primary codes with only CIP-AUT."""
        extractor = DataExtractor()
        text = "Only CIP-AUT: AN123456789012"
        result = extractor.get_primary_codes(text)

        assert result == {
            'cip_sns': None,
            'cip_aut': 'AN123456789012'
        }