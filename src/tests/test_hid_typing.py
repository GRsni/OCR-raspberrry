#!/usr/bin/env python3
"""
Tests for HID typing module.
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
from hid_typing import HIDTyper


class TestHIDTyper:
    """Test HIDTyper class."""

    def test_init(self):
        """Test initialization."""
        typer = HIDTyper()
        assert typer.device_path == "/dev/hidg0"
        assert isinstance(typer.keymap, dict)
        assert 'a' in typer.keymap
        assert '0' in typer.keymap

    def test_init_custom_device(self):
        """Test initialization with custom device path."""
        typer = HIDTyper("/dev/custom")
        assert typer.device_path == "/dev/custom"

    @patch('builtins.open', new_callable=mock_open)
    @patch('hid_typing.time')
    def test_type_text_simple(self, mock_time, mock_file):
        """Test typing simple text."""
        typer = HIDTyper()
        typer.type_text("a")

        # Should have written key press and release
        assert mock_file.call_count == 1
        mock_file.return_value.write.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('hid_typing.time')
    def test_type_text_uppercase(self, mock_time, mock_file):
        """Test typing uppercase text."""
        typer = HIDTyper()
        typer.type_text("A")

        # Should use shift modifier for uppercase
        mock_file.return_value.write.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('hid_typing.time')
    def test_type_text_multiple_chars(self, mock_time, mock_file):
        """Test typing multiple characters."""
        typer = HIDTyper()
        typer.type_text("ab")

        # Should write for each character
        assert mock_file.return_value.write.call_count == 4  # 2 chars * 2 writes each

    @patch('builtins.open')
    def test_type_text_device_not_found(self, mock_open):
        """Test typing when device not found."""
        mock_open.side_effect = FileNotFoundError()
        typer = HIDTyper()

        with pytest.raises(FileNotFoundError):
            typer.type_text("test")

    @patch('hid_typing.HIDTyper.type_text')
    def test_type_codes_both(self, mock_type_text):
        """Test typing both codes."""
        typer = HIDTyper()
        codes = {'cip_sns': '12345678AB123456', 'cip_aut': 'AN123456'}

        typer.type_codes(codes)

        assert mock_type_text.call_count == 2
        mock_type_text.assert_any_call('12345678AB123456')
        mock_type_text.assert_any_call('AN123456')

    @patch('hid_typing.HIDTyper.type_text')
    def test_type_codes_only_sns(self, mock_type_text):
        """Test typing only CIP-SNS code."""
        typer = HIDTyper()
        codes = {'cip_sns': '12345678AB123456', 'cip_aut': None}

        typer.type_codes(codes)

        mock_type_text.assert_called_once_with('12345678AB123456')

    @patch('hid_typing.HIDTyper.type_text')
    def test_type_codes_only_aut(self, mock_type_text):
        """Test typing only CIP-AUT code."""
        typer = HIDTyper()
        codes = {'cip_sns': None, 'cip_aut': 'AN123456'}

        typer.type_codes(codes)

        mock_type_text.assert_called_once_with('AN123456')

    @patch('hid_typing.HIDTyper.type_text')
    def test_type_codes_none(self, mock_type_text):
        """Test typing when no codes."""
        typer = HIDTyper()
        codes = {'cip_sns': None, 'cip_aut': None}

        typer.type_codes(codes)

        mock_type_text.assert_not_called()