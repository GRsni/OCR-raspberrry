#!/bin/bash
# Test runner script that suppresses OpenCV/SWIG deprecation warnings

cd "$(dirname "$0")"
source .venv/bin/activate
cd src

# Suppress OpenCV/SWIG deprecation warnings
export PYTHONWARNINGS=ignore::DeprecationWarning

# Run pytest
python -m pytest "$@"